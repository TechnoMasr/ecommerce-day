/**
 * Dr. Khedr AMA questions (ask-dr-khedr.html) -> private Google Sheet.
 * Same setup as the CRO Talk survey script (cro-talk-survey-sheet.gs).
 *
 * Path of the questions: the page -> TrafficMENA backend
 * (POST /api/ecd/survey-responses, survey "khedr-ama") -> this script ->
 * the sheet. The page never knows this script's URL: it lives only in the
 * server's .env (ECD_SURVEY_KHEDR_SHEET_URL), with a shared secret
 * (ECD_SURVEY_KHEDR_SHEET_SECRET) that this script checks, so nobody else
 * can write to the sheet even if the URL leaks. The script only writes; it
 * never sends questions back. The server stops taking questions after
 * 3 Nov 2026, 11:59 PM Cairo.
 *
 * Setup (once), in the copy of the CRO sheet:
 *  1. Extensions > Apps Script. Delete all the code there and paste this
 *     whole file. Save.
 *  2. Project Settings (gear icon):
 *       Time zone: (GMT+02:00) Cairo.
 *       Script properties: if SURVEY_SECRET is there, edit its value;
 *       if not, add it. Value = the NEW secret the developer gives you
 *       (not the CRO one).
 *  3. Deploy > New deployment > type "Web app".
 *       Execute as: Me
 *       Who has access: Anyone   (not "Anyone with Google account")
 *     Deploy, allow the permissions Google asks for (your own sheet only).
 *  4. Copy the Web app URL (https://script.google.com/macros/s/.../exec)
 *     and send it to the developer (it goes into the server's .env only).
 *  5. After editing this script later: Deploy > Manage deployments > edit
 *     (pencil) > Version: New version > Deploy. The URL stays the same.
 *
 * One row per question (the page makes a new id for every question, and
 * both steps of that question update the same row): "Completed" is FALSE
 * until the email and phone are sent. When a question id changes on the
 * page, change COLUMNS here as well.
 */

var SHEET_NAME = "Responses";

// [answer key, column header]. Answers with other keys are ignored.
var COLUMNS = [
  ["q1", "Q1 Question for Dr. Khedr"],
  ["q2", "Q2 Booking email"],
  ["q3", "Q3 Booking phone"],
];
// Columns to the right of these are for the team (Status, Topic, Moderator
// notes): the script never writes there, so the team's notes stay.
var TEAM = ["Status (team)", "Topic (team)", "Moderator notes (team)"];
var META = ["Response ID", "Started", "Last update", "Completed", "Completed at", "Last step"];
var MAX_LEN = 4000;

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    var data = JSON.parse((e && e.postData && e.postData.contents) || "{}");
    var secret = PropertiesService.getScriptProperties().getProperty("SURVEY_SECRET");
    if (!secret || data.secret !== secret) return reply(false);
    var id = String(data.id || "");
    if (!/^[A-Za-z0-9-]{8,64}$/.test(id)) return reply(false);
    var answers = data.answers && typeof data.answers === "object" ? data.answers : {};

    lock.waitLock(20000);
    var sheet = getSheet();
    var width = META.length + COLUMNS.length;
    var now = new Date();
    var rowIndex = findRow(sheet, id);
    var row = rowIndex
      ? sheet.getRange(rowIndex, 1, 1, width).getValues()[0]
      : new Array(width).fill("");

    var done = data.completed === true;
    row[0] = id;
    if (!row[1]) row[1] = parseDate(data.started) || now;
    row[2] = now;
    row[3] = done;
    if (done && !row[4]) row[4] = now;
    row[5] = safe(data.lastStep);
    // Every answer column is rewritten, so an answer the visitor removed
    // (or a question that no longer shows) is cleared.
    COLUMNS.forEach(function (col, i) {
      row[META.length + i] = Object.prototype.hasOwnProperty.call(answers, col[0])
        ? safe(answers[col[0]])
        : "";
    });

    if (rowIndex) sheet.getRange(rowIndex, 1, 1, width).setValues([row]);
    else sheet.appendRow(row);
    return reply(true);
  } catch (err) {
    return reply(false);
  } finally {
    try {
      lock.releaseLock();
    } catch (ignore) {}
  }
}

// Opening the web app URL in a browser shows {"ok":false}, nothing else.
function doGet() {
  return reply(false);
}

function getSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    var header = META.concat(COLUMNS.map(function (c) { return c[1]; }), TEAM);
    sheet.appendRow(header);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, header.length).setFontWeight("bold");
  }
  return sheet;
}

function findRow(sheet, id) {
  var last = sheet.getLastRow();
  if (last < 2) return 0;
  var ids = sheet.getRange(2, 1, last - 1, 1).getValues();
  for (var i = 0; i < ids.length; i++) {
    if (String(ids[i][0]) === id) return i + 2;
  }
  return 0;
}

// Plain text only, capped, and never read as a formula: a value starting
// with = + - @ (a phone number starts with +) gets a leading apostrophe.
function safe(v) {
  var s = String(v == null ? "" : v).slice(0, MAX_LEN);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function parseDate(v) {
  var d = v ? new Date(v) : null;
  return d && !isNaN(d.getTime()) ? d : null;
}

function reply(ok) {
  return ContentService.createTextOutput(JSON.stringify({ ok: ok })).setMimeType(
    ContentService.MimeType.JSON
  );
}
