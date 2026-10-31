#!/usr/bin/env python3
"""Build the Main Speaker landing pages from the Home page.

One page per Main Speaker, in both languages (user decision, 26 Oct 2026):
    en/speaker-<slug>.html   English, cut from en/index.html
    speaker-<slug>.html      Arabic, cut from index.html (the built Arabic Home)

Each page is the Home page with the speaker's hero and session sections in
place of Home's top sections: the navbar, footer, tickets section (the same
<ecd-tickets> booking block), reviews, FAQ layout and closing section come
from Home, so a change there reaches these pages on the next build.
Run after build-home.py:
    python3 build/build-home.py && python3 build/build-speaker-pages.py
Never edit the four generated pages by hand. Speaker copy lives in SPEAKERS
below; every cut point must match exactly once, so a changed Home page stops
the build instead of producing a broken page.
"""
import html
import json
import pathlib
import re

from common import BASE_URL, ROOT, keep_names_together

CDN = "https://trafficmena.b-cdn.net/ecd/2026/"
MAPS = "https://maps.app.goo.gl/LxbaM9baBAA8t9Pv9"

# ---------------------------------------------------------------- speakers
# Facts come from the announcement posts (user approved them word for word,
# 26 Oct 2026). Session titles and times are not set yet: they show as
# "Announced soon" / "Coming Soon" (hard rules 11 and 12). Final agenda
# (31 Oct 2026): each session has its title (English on both pages, like the
# Agenda) and its time from the admin agenda; change them here too.
SPEAKERS = [
    {
        "slug": "mohamed-hossam-khedr",
        "photo": CDN + "b5b9ad2f-4412-4148-b566-6a7066ab9719.jpg",
        "en": {
            "name": "Dr. Mohamed Hossam Khedr",
            "short": "Dr. Khedr",
            "role": "Business Consultant",
            "title": "Dr. Mohamed Hossam Khedr at ECommerce Day 2026 | TrafficMENA",
            "desc": "Dr. Mohamed Hossam Khedr, Main Speaker at ECommerce Day 2026: an open Q&A on Stage 1 about building a healthy ecommerce business. 5 November 2026, Creativa Innovation Hub, Giza.",
            "lead": "28 years in business management, entrepreneurship and investment across the Arab world. On 5 November he takes Stage 1 for an open Q&A: how to build a healthy ecommerce business, and when to make each move.",
            "facts": [
                ("28 years", "in business, entrepreneurship and investment"),
                ("Dozens", "of companies founded"),
                ("Thousands", "of founders he has shared his experience with"),
            ],
            "session": {
                "eyebrow": "On Stage 1",
                "h2": "Build a Healthy Ecommerce Business, and Know When to Make Each Move",
                "lede": "An open Q&A with Dr. Khedr on business strategy: what a healthy ecommerce business needs, what to do first, and where to slow down before you expand or invest.",
                "format": "Open Q&A",
                "title": "AMA Dr. Hossam Khedr",
                "time": "2:10 PM",
                "topics_h": "What the conversation covers",
                "topics": [
                    "What a healthy ecommerce business looks like, beyond the sales numbers.",
                    "The moves to make now, and the ones to hold until the business is ready.",
                    "How to set priorities when everything feels urgent.",
                    "Growth, investment and expansion decisions, and their timing.",
                    "Keeping the balance between the business, your life and your values.",
                ],
            },
            "focus": {
                "eyebrow": "Your Question",
                "h2": "Get Your Question Ready for Dr. Khedr",
                "lede": "We are collecting questions for Dr. Khedr through a WhatsApp campaign and a public post on our Facebook page. Selected questions become part of the discussion on Stage 1, so watch for our message and the post.",
                "cards": [
                    ("Your company", "A decision on hold, or a problem that keeps coming back."),
                    ("A project you are starting", "A new idea you want to start the right way."),
                    ("An investment decision", "Go in or wait, and on what terms."),
                    ("A hard growth stage", "When growth itself starts causing the problems."),
                    ("Business and life", "Succeeding in business without losing your life and values."),
                ],
            },
            "who_h": "This Session Is for You If",
            "who": [
                "You founded or run a company and face a big decision.",
                "You are starting a new project and want to avoid the early mistakes.",
                "You are weighing an investment or a partnership and have not decided.",
                "Your company is in a growth stage that got harder, not easier.",
            ],
            "about_eyebrow": "About Dr. Khedr",
            "about_h": "28 Years of Building Companies and Investing in Them",
            "about": [
                "Over 28 years in business management, entrepreneurship and investment across the Arab world, Dr. Mohamed Hossam Khedr has founded dozens of companies and sold successful companies valued at millions of dollars. He has worked as an Angel Investor and as a managing partner in Venture Capital, and has shared his experience with thousands of founders and business owners.",
                "Much of what he brings is a way of thinking: seeing the problem more widely, choosing priorities on purpose, and building a stronger business while keeping the balance between work, your life, your values and the goals you actually want to reach.",
            ],
            "final_eyebrow": "5 November · Stage 1",
            "final_h": "Meet Dr. Khedr on Stage 1",
            "faq": [
                ("Which ticket gets me into Dr. Khedr's session?", ["The Standard Pass. His session is on Stage 1, and the Standard Pass gives you full-day access to Stage 1 and Stage 2."]),
                ("How do I send my question?", ["We are collecting questions through a WhatsApp campaign and a public post on our Facebook page. Selected questions become part of the discussion on Stage 1."]),
                ("When is his session?", ["At 2:10 PM on Stage 1. The full program is on the Agenda page."]),
            ],
        },
        "ar": {
            "name": "د. محمد حسام خضر",
            "short": "د. خضر",
            "title": "د. محمد حسام خضر في يوم التجارة الإلكترونية 2026 | TrafficMENA",
            "desc": "د. محمد حسام خضر متحدث رئيسي في يوم التجارة الإلكترونية 2026: جلسة أسئلة مفتوحة على المسرح 1 عن بناء متجر إلكتروني على أساس سليم. 5 نوفمبر 2026، مركز إبداع مصر الرقمية (كريتيفا)، الجيزة.",
            "lead": "28 سنة في الإدارة وريادة الأعمال والاستثمار في العالم العربي. يوم 5 نوفمبر يقف على المسرح 1 في جلسة أسئلة مفتوحة عن بناء شركة قوية في التجارة الإلكترونية، وعن توقيت كل قرار.",
            "facts": [
                ("28 سنة", "في الإدارة وريادة الأعمال والاستثمار"),
                ("عشرات الشركات", "أسسها خلال مسيرته"),
                ("آلاف المؤسسين", "استفادوا من خبرته"),
            ],
            "session": {
                "eyebrow": "على المسرح 1",
                "h2": "كيف تبني متجرك على أساس سليم، ومتى تتخذ كل قرار",
                "lede": "جلسة تسأل فيها د. خضر مباشرة عن استراتيجية شركتك: ما الذي يحتاجه متجرك لينمو دون أن يهتز، وبماذا تبدأ، ومتى تتمهل قبل أن تتوسع أو تستثمر.",
                "format": "أسئلة مفتوحة من الحضور",
                "title": "AMA Dr. Hossam Khedr",
                "time": "2:10 مساءً",
                "topics_h": "ما الذي يدور حوله النقاش",
                "topics": [
                    "كيف تعرف أن شركتك قوية فعلاً، بعيداً عن أرقام المبيعات وحدها.",
                    "الخطوات التي تبدأ بها الآن، والخطوات التي تؤجلها حتى تستعد لها شركتك.",
                    "كيف ترتب أولوياتك حين يبدو كل شيء عاجلاً.",
                    "قرارات النمو والاستثمار والتوسع، وتوقيت كل منها.",
                    "التوازن بين العمل وحياتك وقيمك.",
                ],
            },
            "focus": {
                "eyebrow": "سؤالك",
                "h2": "جهز سؤالك لـ د. خضر",
                "lede": "نجمع الأسئلة الآن عبر حملة على واتساب ومنشور عام على صفحتنا في فيسبوك، والأسئلة التي نختارها تصبح جزءاً من النقاش على المسرح 1. تابع رسالتنا على واتساب والمنشور.",
                "cards": [
                    ("شركتك", "قرار معلق، أو مشكلة تتكرر من وقت لآخر."),
                    ("مشروع تبدأه", "فكرة جديدة وتريد أن تبدأها على الطريق الصحيح."),
                    ("قرار استثماري لم تحسمه", "تدخل أم تنتظر، وبأي شروط."),
                    ("مرحلة نمو صعبة", "حين يصبح النمو نفسه مصدر المشاكل."),
                    ("العمل والحياة", "تنجح في عملك دون أن تخسر حياتك وقيمك."),
                ],
            },
            "who_h": "الجلسة تناسبك إذا",
            "who": [
                "أسست شركة أو تديرها، وأمامك قرار كبير.",
                "تبدأ مشروعاً جديداً وتريد أن تتجنب أخطاء البداية.",
                "تفكر في استثمار أو شراكة ولم تحسم أمرك بعد.",
                "شركتك في مرحلة نمو صارت أصعب بدل أن تصبح أسهل.",
            ],
            "about_eyebrow": "عن د. خضر",
            "about_h": "28 سنة بين بناء الشركات والاستثمار فيها",
            "about": [
                "خلال 28 سنة في الإدارة وريادة الأعمال والاستثمار في العالم العربي، أسس د. محمد حسام خضر عشرات الشركات، وباع شركات ناجحة تقدر قيمتها بملايين الدولارات. عمل مستثمراً في الشركات الناشئة (Angel Investor) وشريكاً مديراً في صندوق رأس مال جريء (Venture Capital)، ونقل خبرته إلى آلاف المؤسسين وأصحاب الشركات.",
                "وجزء كبير مما يقدمه هو طريقة التفكير نفسها: أن ترى المشكلة من زاوية أوسع، وتختار أولوياتك بوعي، وتبني شركة أقوى دون أن تخسر التوازن بين العمل وحياتك وقيمك والأهداف التي تريدها فعلاً.",
            ],
            "final_eyebrow": "5 نوفمبر، المسرح 1",
            "final_h": "احضر جلسة د. خضر على المسرح 1",
            "faq": [
                ("أي تذكرة تدخلني جلسة د. خضر؟", ["التذكرة الأساسية (Standard Pass). جلسته على المسرح 1، والتذكرة الأساسية تدخلك المسرح 1 والمسرح 2 طوال اليوم."]),
                ("كيف أرسل سؤالي؟", ["نجمع الأسئلة عبر حملة على واتساب ومنشور عام على صفحتنا في فيسبوك، والأسئلة التي نختارها تصبح جزءاً من النقاش على المسرح 1."]),
                ("متى موعد جلسته؟", ["الساعة 2:10 مساءً على المسرح 1، والبرنامج كامل في صفحة الأجندة."]),
            ],
        },
    },
    {
        "slug": "mohamed-neamatalla",
        "photo": CDN + "9b32905f-74dd-40db-b28c-e37801592b5d.jpg",
        "en": {
            "name": "Mohamed Neamatalla",
            "short": "Mohamed Neamatalla",
            "role": "Founder & CEO of Optimizers",
            "title": "Mohamed Neamatalla at ECommerce Day 2026 | TrafficMENA",
            "desc": "Mohamed Neamatalla, Founder & CEO of Optimizers, on Stage 1 at ECommerce Day 2026: grow ecommerce revenue with CRO before you raise ad spend. 5 November 2026, Creativa Innovation Hub, Giza.",
            "lead": "More than 20 years in digital marketing and ecommerce across Egypt, the Gulf and the US. On 5 November he takes Stage 1 to talk about growing from the traffic your store already gets, before you raise the ad budget.",
            "facts": [
                ("20+ years", "in digital marketing and ecommerce"),
                ("3 markets", "Egypt, the Gulf and the US"),
                ("Hundreds", "of companies he helped grow profit"),
            ],
            "session": {
                "eyebrow": "On Stage 1",
                "h2": "Grow Revenue With CRO Before You Spend More on Ads",
                "lede": "A Stage 1 session on conversion rate optimization (CRO): how ecommerce brands get more orders and revenue out of the traffic they already have.",
                "format": "",
                "title": "CRO By Mohamed Neamatalla",
                "time": "6:15 PM",
                "topics_h": "What the session is about",
                "topics": [
                    "Finding the growth that already sits inside your store.",
                    "Improving the buying experience and the conversion rate.",
                    "Reading customer behaviour to decide what to fix first.",
                    "When a bigger ad budget is not the answer.",
                ],
            },
            "focus": {
                "eyebrow": "Before You Raise the Ad Budget",
                "h2": "The Traffic Is There. The Problem Is What Happens Next",
                "lede": "Many stores answer slow growth by spending more on ads. Mohamed starts from a different question: why don't the people already visiting your store buy?",
                "cards": [
                    ("Visitors who leave", "Where they stop, and why."),
                    ("Friction in the buying journey", "Steps that slow customers down or confuse them."),
                    ("A conversion rate you can lift", "More orders from the same ad budget."),
                    ("Decisions based on behaviour", "Instead of guessing what to change."),
                ],
            },
            "who_h": "This Session Is for You If",
            "who": [
                "You run an online store, pay for ads and do not see the sales you expect.",
                "You work in marketing, growth or media buying.",
                "You look after the customer experience or the product in a store.",
                "You work at an agency that serves ecommerce brands.",
            ],
            "about_eyebrow": "About Mohamed Neamatalla",
            "about_h": "One of the First to Bring CRO to Arabic",
            "about": [
                "More than 20 years in digital marketing and ecommerce across Egypt, the Gulf and the US, helping hundreds of companies and startups grow profit and expand into new industries and markets. He was one of the first to present CRO in Arabic, and helped spread it and make it better understood across the Arab world.",
                "He is the Founder & CEO of Optimizers, a conversion rate optimization agency for ecommerce brands. Optimizers helps online stores get more value from their current traffic and improve the buying experience and conversion rates, so growth does not depend only on more ad spend.",
            ],
            "final_eyebrow": "5 November · Stage 1",
            "final_h": "Meet Mohamed Neamatalla on Stage 1",
            "faq": [
                ("Which ticket gets me into Mohamed Neamatalla's session?", ["The Standard Pass. His session is on Stage 1, and the Standard Pass gives you full-day access to Stage 1 and Stage 2."]),
                ("What is the title of his session, and when is it?", ["\"CRO By Mohamed Neamatalla\", at 6:15 PM on Stage 1. The full program is on the Agenda page."]),
            ],
        },
        "ar": {
            "name": "محمد نعمة الله",
            "short": "محمد نعمة الله",
            "title": "محمد نعمة الله في يوم التجارة الإلكترونية 2026 | TrafficMENA",
            "desc": "محمد نعمة الله، مؤسس Optimizers ورئيسها التنفيذي، على المسرح 1 في يوم التجارة الإلكترونية 2026: ارفع مبيعات متجرك بالـ CRO قبل أن تزيد ميزانية الإعلانات. 5 نوفمبر 2026، مركز إبداع مصر الرقمية (كريتيفا)، الجيزة.",
            "lead": "أكثر من 20 سنة في التسويق الرقمي والتجارة الإلكترونية في مصر والخليج وأمريكا. يوم 5 نوفمبر يقف على المسرح 1 ليتكلم عن زيادة المبيعات من الزوار الذين يدخلون متجرك اليوم، قبل أن تزيد ميزانية الإعلانات.",
            "facts": [
                ("+20 سنة", "في التسويق الرقمي والتجارة الإلكترونية"),
                ("3 أسواق", "مصر والخليج وأمريكا"),
                ("مئات الشركات", "ساعدها على زيادة الأرباح"),
            ],
            "session": {
                "eyebrow": "على المسرح 1",
                "h2": "ارفع مبيعاتك بالـ CRO قبل أن تزيد ميزانية الإعلانات",
                "lede": "جلسة على المسرح 1 عن تحسين معدل التحويل (CRO): كيف يحصل متجرك على طلبات أكثر من الزوار الذين يدخلونه بالفعل.",
                "format": "",
                "title": "CRO By Mohamed Neamatalla",
                "time": "6:15 مساءً",
                "topics_h": "ما الذي تتناوله الجلسة",
                "topics": [
                    "فرص النمو الموجودة أصلاً داخل متجرك.",
                    "تحسين تجربة الشراء ومعدل التحويل.",
                    "فهم سلوك العميل لتعرف بماذا تبدأ.",
                    "متى لا تكون زيادة ميزانية الإعلانات هي الحل.",
                ],
            },
            "focus": {
                "eyebrow": "قبل أن تزيد ميزانية الإعلانات",
                "h2": "الزوار موجودون. المشكلة فيما يحدث بعد دخولهم",
                "lede": "متاجر كثيرة تعالج بطء النمو بإنفاق أكبر على الإعلانات. محمد نعمة الله يبدأ من سؤال آخر: لماذا لا يشتري من يزور متجرك الآن؟",
                "cards": [
                    ("زوار يخرجون دون أن يشتروا", "أين يتوقفون، ولماذا."),
                    ("عوائق في تجربة الشراء", "خطوات تبطئ العميل أو تربكه."),
                    ("معدل تحويل يمكن رفعه", "طلبات أكثر من ميزانية الإعلانات نفسها."),
                    ("قرارات تعتمد على سلوك العميل", "لا على التخمين فيما يجب تغييره."),
                ],
            },
            "who_h": "الجلسة تناسبك إذا",
            "who": [
                "تدير متجراً إلكترونياً وتنفق على الإعلانات ولا ترى المبيعات التي تتوقعها.",
                "تعمل في التسويق أو شراء الإعلانات (Media Buying).",
                "تتولى تجربة العميل أو المنتج في متجر إلكتروني.",
                "تعمل في وكالة تخدم متاجر إلكترونية.",
            ],
            "about_eyebrow": "عن محمد نعمة الله",
            "about_h": "من أوائل من قدموا الـ CRO بالعربي",
            "about": [
                "أكثر من 20 سنة في التسويق الرقمي والتجارة الإلكترونية في أسواق مصر والخليج وأمريكا، ساعد خلالها مئات الشركات الكبيرة والناشئة على زيادة الأرباح والتوسع في صناعات وأسواق مختلفة. وهو من أوائل من قدموا تحسين معدل التحويل (CRO) بالعربي، وساعد على انتشاره وفهمه في العالم العربي.",
                "وهو مؤسس Optimizers ورئيسها التنفيذي (Founder & CEO)، وهي وكالة متخصصة في الـ CRO للمتاجر الإلكترونية. تساعد Optimizers المتاجر على أن تبيع أكثر لمن يزورها الآن، عبر تحسين تجربة الشراء ومعدلات التحويل، حتى لا يعتمد النمو على زيادة الإنفاق على الإعلانات وحده.",
            ],
            "final_eyebrow": "5 نوفمبر، المسرح 1",
            "final_h": "احضر جلسة محمد نعمة الله على المسرح 1",
            "faq": [
                ("أي تذكرة تدخلني جلسة محمد نعمة الله؟", ["التذكرة الأساسية (Standard Pass). جلسته على المسرح 1، والتذكرة الأساسية تدخلك المسرح 1 والمسرح 2 طوال اليوم."]),
                ("ما عنوان جلسته، ومتى موعدها؟", ["«CRO By Mohamed Neamatalla»، الساعة 6:15 مساءً على المسرح 1، والبرنامج كامل في صفحة الأجندة."]),
            ],
        },
    },
]

# ------------------------------------------------------- fixed page text
UI = {
    "en": {
        "pill": "Main Speaker",
        "speakers": "Speakers",
        "home": "ECommerce Day",
        "date": "5 November 2026",
        "venue": "Creativa Innovation Hub, Giza",
        "stage": "Stage 1",
        "cta": "Get Your Ticket",
        "about_session": "About the Session",
        "float_sub": "Stage 1, ECommerce Day 2026",
        "room": "Room",
        "format": "Format",
        "title_l": "Session title",
        "title_v": "Announced soon",
        "time_l": "Time",
        "time_v": "Coming Soon",
        "day_eyebrow": "The Rest of the Day",
        "day_h": "One Ticket, Both Stages, the Whole Day",
        "day_p": "The Standard Pass gives you Stage 1 and Stage 2 from 10:30 AM to 7:30 PM: keynotes, panels, case studies and time to meet store owners, platforms and service companies.",
        "day_cards": [
            ("Stage 1 and Stage 2", "Sessions all day. The Standard Pass covers both."),
            ("Registration 9:30 AM", "The program runs from 10:30 AM to 7:30 PM."),
            ("Expo Area", "Companies showing ecommerce services and tools."),
            ("Networking", "Open time to meet store owners, platforms and partners."),
        ],
        "agenda_btn": "View the Agenda",
        "speakers_btn": "Meet All Speakers",
        "final_sub": "Get the Standard Pass and spend the whole day on Stage 1 and Stage 2.",
        "photo_alt": "{name}, Main Speaker at ECommerce Day 2026",
        "locale": "en_US",
    },
    "ar": {
        "pill": "متحدث رئيسي",
        "speakers": "المتحدثون",
        "home": "يوم التجارة الإلكترونية",
        "date": "5 نوفمبر 2026",
        "venue": "مركز إبداع مصر الرقمية (كريتيفا)، الجيزة",
        "stage": "المسرح 1",
        "cta": "احجز تذكرتك",
        "about_session": "عن الجلسة",
        "float_sub": "المسرح 1، يوم التجارة الإلكترونية 2026",
        "room": "القاعة",
        "format": "شكل الجلسة",
        "title_l": "عنوان الجلسة",
        "title_v": "يعلن قريباً",
        "time_l": "الموعد",
        "time_v": "يعلن قريباً",
        "day_eyebrow": "باقي اليوم",
        "day_h": "تذكرة واحدة تدخلك المسرحين طوال اليوم",
        "day_p": "التذكرة الأساسية (Standard Pass) تدخلك المسرح 1 والمسرح 2 من 10:30 صباحاً حتى 7:30 مساءً: كلمات رئيسية، وجلسات نقاشية، ودراسات حالة، ووقت تقابل فيه أصحاب المتاجر والمنصات وشركات الخدمات.",
        "day_cards": [
            ("المسرح 1 والمسرح 2", "جلسات طوال اليوم، والتذكرة الأساسية تشمل المسرحين معاً."),
            ("التسجيل 9:30 صباحاً", "والبرنامج من 10:30 صباحاً حتى 7:30 مساءً."),
            ("منطقة المعرض (Expo Area)", "شركات تعرض خدماتها وأدواتها للتجارة الإلكترونية."),
            ("التعارف", "وقت مفتوح تقابل فيه أصحاب متاجر ومنصات وشركات خدمات."),
        ],
        "agenda_btn": "شاهد الأجندة",
        "speakers_btn": "كل المتحدثين",
        "final_sub": "احجز التذكرة الأساسية، واحضر اليوم كله على المسرح 1 والمسرح 2.",
        "photo_alt": "{name}، متحدث رئيسي في يوم التجارة الإلكترونية 2026",
        "locale": "ar_EG",
    },
}

# Home FAQ answers reused on every speaker page: venue, start time, refunds.
FAQ_TAIL = {
    "en": """          {
            q: "When and where is the event?",
            a: [
              {
                p: "ECommerce Day will take place on 5 November 2026 at Creativa Innovation Hub, Giza.",
              },
              {
                p: "The full address, map, entry instructions, and transportation details will be shared with confirmed attendees before the event.",
              },
            ],
          },
          {
            q: "What time does the event start?",
            a: [
              {
                p: "Registration opens at 9:30 AM, and the stage program begins at 10:30 AM.",
              },
              {
                p: "Attendees are encouraged to arrive early to complete check-in and explore the venue before the first sessions begin.",
              },
            ],
          },
          {
            q: "Can I request a refund or transfer my ticket?",
            a: [
              {
                p: "A full refund is available until the end of 30 October 2026, five days before the event.",
              },
              {
                p: "To request a refund, email info@trafficmena.com before the deadline using the email associated with your booking.",
              },
              {
                p: "Requests received after this date cannot be accepted. Tickets are non-transferable and cannot be reassigned to another attendee.",
              },
              {
                p: "Approved refunds will be returned through the original payment method.",
              },
              { contact: "For assistance, contact" },
            ],
          },
""",
    "ar": """          {
            q: "متى وأين يقام اليوم؟",
            a: [
              {
                p: "يوم الخميس 5 نوفمبر 2026، في مركز إبداع مصر الرقمية (كريتيفا) بالجيزة. قبل الفعالية نرسل للحضور المؤكدين العنوان الكامل والخريطة وتعليمات الدخول والمواصلات.",
              },
            ],
          },
          {
            q: "متى يبدأ اليوم؟",
            a: [
              {
                p: "يفتح التسجيل الساعة 9:30 صباحاً، ويبدأ برنامج المسرح الساعة 10:30. تعال مبكراً لتنهي التسجيل وتعرف المكان قبل أول جلسة.",
              },
            ],
          },
          {
            q: "هل يمكنني استرداد ثمن التذكرة أو نقلها لشخص آخر؟",
            a: [
              {
                p: "الاسترداد الكامل متاح حتى نهاية يوم 30 أكتوبر 2026، أي قبل الفعالية بخمسة أيام. أرسل طلبك إلى info@trafficmena.com من البريد الإلكتروني الذي حجزت به، ويعود المبلغ بوسيلة الدفع نفسها. بعد هذا التاريخ لا نقبل طلبات الاسترداد.",
              },
              { p: "التذاكر شخصية ولا يمكن نقلها لحاضر آخر." },
              { contact: "لأي مساعدة:" },
            ],
          },
""",
}

SPEAKER_CSS = """
      /* ============ SPEAKER PAGE (build/build-speaker-pages.py) ============ */
      #session,
      #tickets {
        scroll-margin-top: var(--ecd-nav-h, 72px);
      }
      .sp-hero .hero-grid {
        grid-template-columns: 1.1fr 0.9fr;
      }
      .sp-pill {
        display: inline-flex;
        align-items: center;
        background: #101010;
        color: #05ef62;
        border-radius: 999px;
        padding: 7px 14px;
        font-family: "JetBrains Mono", monospace;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 18px;
      }
      .sp-name {
        font-size: clamp(38px, 5vw, 58px);
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 10px;
      }
      .sp-role {
        font-size: 16px;
        font-weight: 600;
        color: var(--ink-soft);
        margin-bottom: 20px;
      }
      .sp-hero .hero-lead {
        margin-bottom: 24px;
      }
      .sp-facts {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        margin-bottom: 24px;
      }
      .sp-fact {
        border: 1px solid var(--line-strong);
        border-radius: 12px;
        padding: 14px 16px;
        background: var(--white);
      }
      .sp-fact-value {
        font-size: 22px;
        font-weight: 800;
        line-height: 1.2;
        color: #101010;
      }
      .sp-fact-label {
        font-size: 13px;
        line-height: 1.5;
        color: var(--ink-soft);
        margin-top: 4px;
      }
      .sp-hero .badges {
        margin-bottom: 26px;
      }
      .sp-hero .hero-cta-row {
        margin-bottom: 0;
      }
      .sp-dot {
        flex: none;
        width: 8px;
        height: 8px;
        border-radius: 2px;
        background: #101010;
      }
      .sp-hero .hero-media {
        max-width: 460px;
        width: 100%;
        margin-inline-start: auto;
      }
      .sp-hero .hero-media-frame {
        aspect-ratio: 4 / 5;
        background: var(--soft);
      }
      .sp-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 28px;
      }
      .sp-meta li {
        background: var(--white);
        border: 1px solid var(--line-strong);
        border-radius: 12px;
        padding: 12px 16px;
        min-width: 150px;
      }
      .sp-meta-label {
        display: block;
        font-family: "JetBrains Mono", monospace;
        font-size: 11px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #6b747e;
        margin-bottom: 4px;
      }
      .sp-meta-value {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        font-size: 15px;
        color: #101010;
      }
      .sp-panel {
        background: var(--white);
        border: 1px solid var(--line-strong);
        border-radius: var(--radius);
        padding: 26px 28px;
        max-width: 860px;
      }
      .sp-panel h3 {
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 14px;
      }
      .sp-list li {
        display: flex;
        gap: 12px;
        align-items: flex-start;
        font-size: 16px;
        line-height: 1.7;
        color: #1f2630;
        padding: 6px 0;
      }
      .sp-list svg {
        flex: none;
        margin-top: 5px;
      }
      .sp-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
      }
      .sp-card {
        background: var(--white);
        border: 1px solid var(--line-strong);
        border-radius: var(--radius);
        padding: 22px 20px;
        transition: box-shadow 0.2s;
      }
      .sp-card:hover {
        box-shadow: 0 14px 40px rgba(16, 16, 16, 0.08);
      }
      .sp-card-num {
        font-family: "JetBrains Mono", monospace;
        font-size: 12px;
        letter-spacing: 0.1em;
        color: #04c44e;
        margin-bottom: 10px;
      }
      .sp-card-title {
        font-weight: 800;
        font-size: 16px;
        line-height: 1.35;
        margin-bottom: 6px;
      }
      .sp-card-line {
        font-size: 14px;
        line-height: 1.6;
        color: var(--ink-soft);
      }
      .sp-about p {
        font-size: 16px;
        line-height: 1.8;
        color: #1f2630;
        margin-bottom: 16px;
        max-width: 64ch;
      }
      .sp-day-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 8px;
      }
      /* Sponsors on a speaker page: one compact block of logos per line */
      #sponsors.sp-compact .featured-line,
      #sponsors.sp-compact .supported-asset,
      #sponsors.sp-compact .featured-card-actions {
        display: none;
      }
      #sponsors.sp-compact .featured-card {
        padding: 12px;
      }
      #sponsors.sp-compact .partner-logo-slot {
        height: 96px;
        border: 0;
        padding: 6px 10px;
      }
      #sponsors.sp-compact .size-main .partner-logo-slot {
        height: 140px;
      }
      #sponsors.sp-compact .tier-grid.size-main {
        grid-template-columns: minmax(0, 360px);
      }
      #sponsors.sp-compact .tier-grid.size-large {
        grid-template-columns: repeat(4, minmax(0, 1fr));
      }
      #sponsors.sp-compact .partner-mini {
        height: 84px;
      }
      #sponsors.sp-compact .tier-row + .tier-row {
        margin-top: 32px;
      }
      /* Arabic: Arabic face for labels, no capitals or letter-spacing */
      html[lang="ar"] .sp-pill,
      html[lang="ar"] .sp-meta-label,
      html[lang="ar"] .sp-card-num {
        font-family: "IBM Plex Sans Arabic", "Manrope", sans-serif;
        letter-spacing: 0;
        text-transform: none;
      }
      html[lang="ar"] .sp-pill,
      html[lang="ar"] .sp-meta-label {
        font-size: 13px;
      }
      html[lang="ar"] .sp-name {
        letter-spacing: 0;
        line-height: 1.3;
      }
      html[lang="ar"] .sp-role span {
        unicode-bidi: isolate;
      }
      @media (max-width: 900px) {
        .sp-hero .hero-grid {
          grid-template-columns: 1fr;
        }
        .sp-hero .hero-media {
          max-width: 380px;
          margin-inline: auto;
        }
        #sponsors.sp-compact .tier-grid.size-large {
          grid-template-columns: repeat(3, minmax(0, 1fr));
        }
      }
      @media (max-width: 600px) {
        .sp-facts {
          grid-template-columns: 1fr;
          gap: 8px;
        }
        .sp-fact {
          display: flex;
          align-items: baseline;
          gap: 10px;
          padding: 12px 14px;
        }
        .sp-fact-label {
          margin-top: 0;
        }
        .sp-meta li {
          flex: 1 1 calc(50% - 12px);
          min-width: 0;
        }
        .sp-panel {
          padding: 20px;
        }
        .sp-day-actions .btn {
          width: 100%;
        }
        #sponsors.sp-compact .tier-grid.size-large {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }
      }
"""

CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#04C44E" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'
CAL = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2" /><path d="M16 3v4M8 3v4M3 10h18" /></svg>'
PIN = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-6.5 7-11a7 7 0 1 0-14 0c0 4.5 7 11 7 11Z" /><circle cx="12" cy="10" r="2.5" /></svg>'
MIC = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#04C44E" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="2" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4M9 22h6"/></svg>'
ARROW = '<svg{flip} width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg>'
DAY_ICONS = [
    '<rect x="9" y="2" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4M9 22h6"/>',
    '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    '<circle cx="9" cy="8" r="3"/><path d="M2 20c0-3.3 3-6 7-6s7 2.7 7 6"/><circle cx="17" cy="9" r="2.4"/><path d="M15.5 14c2.9.3 5.5 2.6 5.5 6"/>',
]


def e(t):
    return html.escape(t, quote=True)


def js(t):
    return json.dumps(t, ensure_ascii=False)


def once(s, old, new, label):
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"[{label}] expected 1 match, found {n}: {old[:90]!r}")
    return s.replace(old, new)


def once_re(s, pattern, new, label, flags=0):
    found = re.findall(pattern, s, flags)
    if len(found) != 1:
        raise SystemExit(f"[{label}] expected 1 match, found {len(found)}: {pattern[:90]!r}")
    return re.sub(pattern, lambda m: new, s, count=1, flags=flags)


def cut(s, start, end, label):
    """Return (before, middle, after) around start..end (end excluded)."""
    if s.count(start) != 1 or s.count(end) != 1:
        raise SystemExit(f"[{label}] marker not found once: {start[:60]!r} / {end[:60]!r}")
    i = s.index(start)
    j = s.index(end)
    if j < i:
        raise SystemExit(f"[{label}] markers out of order")
    return s[:i], s[i:j], s[j:]


def page_urls(slug):
    file = f"speaker-{slug}.html"
    return BASE_URL + file, BASE_URL + "en/" + file


def hero(sp, lang, c, ui):
    ar = lang == "ar"
    flip = ' class="ecd-flip"' if ar else ''
    if ar:
        role = f'<span dir="ltr">{e(sp["en"]["name"])} · {e(sp["en"]["role"])}</span>'
    else:
        role = e(c["role"])
    facts = "".join(
        f"""
                <li class="sp-fact">
                  <div class="sp-fact-value">{e(v)}</div>
                  <div class="sp-fact-label">{e(l)}</div>
                </li>"""
        for v, l in c["facts"]
    )
    return f"""      <!-- ============ SPEAKER HERO ============ -->
      <section class="hero sp-hero">
        <div class="container">
          <div class="hero-grid">
            <div class="hero-text">
              <span class="sp-pill">{e(ui["pill"])}</span>
              <h1 class="sp-name">{e(c["name"])}</h1>
              <p class="sp-role">{role}</p>
              <p class="hero-lead">{e(c["lead"])}</p>
              <ul class="sp-facts">{facts}
              </ul>
              <div class="badges">
                <span class="badge">{CAL}{e(ui["date"])}</span>
                <span class="badge">{PIN}{e(ui["venue"])}</span>
                <span class="badge"><span class="sp-dot" aria-hidden="true"></span>{e(ui["stage"])}</span>
              </div>
              <div class="hero-cta-row">
                <a href="#tickets" class="btn btn-primary btn-lg">{e(ui["cta"])} {ARROW.format(flip=flip)}</a>
                <a href="#session" class="link-underline">{e(ui["about_session"])}</a>
              </div>
            </div>

            <div class="hero-media">
              <div class="hero-media-frame">
                <img
                  src="{sp["photo"]}"
                  width="1200"
                  height="1500"
                  alt="{e(ui["photo_alt"].format(name=c["name"]))}"
                  fetchpriority="high"
                />
              </div>
              <div class="hero-media-float">
                {MIC}
                <div>
                  <div class="float-title">{e(ui["pill"])}</div>
                  <div class="float-sub">{e(ui["float_sub"])}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
"""


def session(c, ui):
    s = c["session"]
    meta = [(ui["room"], f'<span class="sp-dot" aria-hidden="true"></span>{e(ui["stage"])}')]
    if s["format"]:
        meta.append((ui["format"], e(s["format"])))
    meta.append((ui["title_l"], e(s.get("title") or ui["title_v"])))
    meta.append((ui["time_l"], e(s.get("time") or ui["time_v"])))
    meta_html = "".join(
        f"""
            <li><span class="sp-meta-label">{e(l)}</span><span class="sp-meta-value">{v}</span></li>"""
        for l, v in meta
    )
    topics = "".join(f"\n              <li>{CHECK}<span>{e(t)}</span></li>" for t in s["topics"])
    return f"""
      <!-- ============ SESSION ============ -->
      <section id="session" class="section section-soft">
        <div class="container">
          <div class="eyebrow">{e(s["eyebrow"])}</div>
          <h2 class="section-title" data-reveal>{e(s["h2"])}</h2>
          <p class="section-sub" data-reveal>{e(s["lede"])}</p>
          <ul class="sp-meta">{meta_html}
          </ul>
          <div class="sp-panel">
            <h3>{e(s["topics_h"])}</h3>
            <ul class="sp-list">{topics}
            </ul>
          </div>
        </div>
      </section>
"""


def focus(c):
    f = c["focus"]
    cards = "".join(
        f"""
            <div class="sp-card" data-reveal>
              <div class="sp-card-num">{i + 1:02d}</div>
              <div class="sp-card-title">{e(t)}</div>
              <div class="sp-card-line">{e(l)}</div>
            </div>"""
        for i, (t, l) in enumerate(f["cards"])
    )
    return f"""
      <!-- ============ SPEAKER FOCUS ============ -->
      <section class="section">
        <div class="container">
          <div class="eyebrow">{e(f["eyebrow"])}</div>
          <h2 class="section-title" data-reveal>{e(f["h2"])}</h2>
          <p class="section-sub" data-reveal>{e(f["lede"])}</p>
          <div class="sp-cards">{cards}
          </div>
        </div>
      </section>
"""


def about(c):
    paras = "".join(f"\n              <p>{e(p)}</p>" for p in c["about"])
    who = "".join(f"\n                <li>{CHECK}<span>{e(w)}</span></li>" for w in c["who"])
    return f"""
      <!-- ============ ABOUT THE SPEAKER ============ -->
      <section class="section section-soft">
        <div class="container">
          <div class="split">
            <div class="sp-about">
              <div class="eyebrow">{e(c["about_eyebrow"])}</div>
              <h2 class="section-title" data-reveal>{e(c["about_h"])}</h2>{paras}
            </div>
            <div class="sp-panel">
              <h3>{e(c["who_h"])}</h3>
              <ul class="sp-list">{who}
              </ul>
            </div>
          </div>
        </div>
      </section>
"""


def day(lang, ui):
    link_attr = ' data-ar-link' if lang == "ar" else ''
    cards = "".join(
        f"""
              <div class="feature-card" data-reveal>
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#1E2422" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{DAY_ICONS[i]}</svg>
                <div class="feature-title">{e(t)}</div>
                <div class="feature-line">{e(l)}</div>
              </div>"""
        for i, (t, l) in enumerate(ui["day_cards"])
    )
    return f"""
      <!-- ============ THE REST OF THE DAY ============ -->
      <section class="section">
        <div class="container">
          <div class="split">
            <div>
              <div class="eyebrow">{e(ui["day_eyebrow"])}</div>
              <h2 class="section-title" data-reveal>{e(ui["day_h"])}</h2>
              <p class="body-lg">{e(ui["day_p"])}</p>
              <div class="sp-day-actions">
                <a href="agenda.html"{link_attr} class="btn btn-primary">{e(ui["agenda_btn"])}</a>
                <a href="speakers.html"{link_attr} class="btn btn-outline-dark">{e(ui["speakers_btn"])}</a>
              </div>
            </div>
            <div class="feature-grid">{cards}
            </div>
          </div>
        </div>
      </section>
"""


def faq_js(c, lang):
    items = ""
    for q, answers in c["faq"]:
        ps = "".join(
            f"""
              {{
                p: {js(a)},
              }},"""
            for a in answers
        )
        items += f"""          {{
            q: {js(q)},
            a: [{ps}
            ],
          }},
"""
    return "        var faqData = [\n" + items + FAQ_TAIL[lang] + "        ];\n"


def head_extra(sp, lang, c, ui, prefix, bc_tag):
    ar_url, en_url = page_urls(sp["slug"])
    url = ar_url if lang == "ar" else en_url
    og_img = f"{BASE_URL}assets/speakers/{sp['slug']}-{lang}.png"
    home = BASE_URL if lang == "ar" else BASE_URL + "en/"
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["home"], "item": home},
            {"@type": "ListItem", "position": 2, "name": ui["speakers"], "item": home + "speakers.html"},
            {"@type": "ListItem", "position": 3, "name": c["name"]},
        ],
    }
    ld = json.dumps(crumbs, ensure_ascii=False, indent=2)
    return f"""    <link rel="canonical" href="{url}" />
    <link rel="alternate" hreflang="ar" href="{ar_url}" />
    <link rel="alternate" hreflang="en" href="{en_url}" />
    <link rel="alternate" hreflang="x-default" href="{ar_url}" />
    <meta
      name="description"
      content="{e(c["desc"])}"
    />
    <!-- Read by ecd-analytics.js: page_type ecd_speaker + speaker_name -->
    <meta name="ecd-speaker" content="{e(sp["en"]["name"])}" />
    <meta property="og:type" content="profile" />
    <meta property="og:site_name" content="TrafficMENA" />
    <meta property="og:locale" content="{ui["locale"]}" />
    <meta property="og:title" content="{e(c["title"])}" />
    <meta property="og:description" content="{e(c["desc"])}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{og_img}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="{e(ui["photo_alt"].format(name=c["name"]))}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:image" content="{og_img}" />
    <script type="application/ld+json">
{ld}
    </script>
""", f'    <script src="{prefix}breadcrumbs.js?v={bc_tag}" defer></script>\n'


def build(sp, lang, src, bc_tag):
    c = sp[lang]
    ui = UI[lang]
    label = f"{sp['slug']}/{lang}"
    prefix = "" if lang == "ar" else "../"
    s = src

    s = once(s, "<!doctype html>\n", "<!doctype html>\n<!-- Generated by build/build-speaker-pages.py from the Home page. Do not edit by hand. -->\n", label)

    # ---------- <head> ----------
    s = once_re(s, r"<title>[^<]*</title>", f"<title>{e(c['title'])}</title>", label)
    extra, bc_script = head_extra(sp, lang, c, ui, prefix, bc_tag)
    s = once_re(
        s,
        r'    <link rel="canonical"[^\n]*\n(?:    <link rel="alternate"[^\n]*\n){3}    <meta\n      name="description"\n      content="[^"]*"\n    />\n',
        extra,
        label,
    )
    # The speaker photo is the hero image (LCP): preload it instead of Home's
    s = once_re(
        s,
        r"    <!-- Hero image is the LCP element[^\n]*\n    <link\n      rel=\"preload\"\n      as=\"image\"[\s\S]*?\n    />\n",
        f'    <!-- Speaker photo is the hero image (LCP): start downloading it first -->\n    <link rel="preload" as="image" href="{sp["photo"]}" fetchpriority="high" />\n',
        label,
    )
    m = re.search(r'    <script src="(?:\.\./)?navbar\.js\?v=[^"]+" defer></script>\n', s)
    if not m or len(re.findall(r'navbar\.js\?v=', s)) != 1:
        raise SystemExit(f"[{label}] navbar.js tag not found once")
    s = s[: m.end()] + bc_script + s[m.end():]
    i = s.rindex("    </style>\n  </head>")
    s = s[:i] + SPEAKER_CSS.lstrip("\n").rstrip() + "\n" + s[i:]

    # ---------- body ----------
    trail = json.dumps([[ui["home"], "index.html"], [ui["speakers"], "speakers.html"], [c["name"]]], ensure_ascii=False)
    s = once(
        s,
        '<site-navbar current="home"></site-navbar>\n',
        '<site-navbar current="speakers"></site-navbar>\n'
        f"    <ecd-breadcrumb id=\"ecdBreadcrumb\" data-trail='{trail}' style=\"display:block;min-height:44px\"></ecd-breadcrumb>\n",
        label,
    )

    # Home sponsors section, kept as a compact logo block
    _, sponsors, _ = cut(s, "      <!-- ============ SPONSORS ============ -->", "      <!-- ============ SPEAKERS ============ -->", label)
    sponsors = once(sponsors, '<section id="sponsors" class="section section-soft">', '<section id="sponsors" class="section section-soft sp-compact">', label)

    # Home hero ... outcomes out; speaker sections in (tickets onward stay)
    before, _, after = cut(s, "      <!-- ============ HERO ============ -->", "      <!-- ============ TICKETS (shared: tickets-section.js) ============ -->", label)
    s = before + hero(sp, lang, c, ui) + session(c, ui) + focus(c) + about(c) + day(lang, ui) + "\n" + sponsors + after

    # Closing section: speaker heading, Get Your Ticket stays on this page
    before, final, after = cut(s, "      <!-- ============ FINAL CTA ============ -->", "    </main>", label)
    final = once_re(final, r'<div class="eyebrow">[^<]*</div>', f'<div class="eyebrow">{e(c["final_eyebrow"])}</div>', label)
    final = once_re(final, r'<h2 class="final-cta-title">[^<]*</h2>', f'<h2 class="final-cta-title">{e(c["final_h"])}</h2>', label)
    final = once_re(final, r'<p class="final-cta-sub">[\s\S]*?</p>', f'<p class="final-cta-sub">\n            {e(ui["final_sub"])}\n          </p>', label)
    final = once_re(final, r'<a href="tickets\.html"(?: data-ar-link)? class="btn btn-primary">', '<a href="#tickets" class="btn btn-primary">', label)
    s = before + final + after

    # Phone bottom bar: Get Ticket scrolls to the tickets on this page
    before, bar, after = cut(s, '    <div class="mobile-cta" id="mobileCta"', "    <script>\n", label)
    bar = once_re(bar, r'<a href="tickets\.html"(?: data-ar-link)? class="btn btn-primary">', '<a href="#tickets" class="btn btn-primary">', label)
    s = before + bar + after

    # FAQ: speaker questions first, then venue, times and refunds
    i = s.index("        var faqData = [\n")
    j = s.index("        ];\n", i) + len("        ];\n")
    s = s[:i] + faq_js(c, lang) + s[j:]

    for left in ['id="countdown"', 'id="speakersTrack"', 'id="communityMarquee"', "hero-home-"]:
        if left in s:
            raise SystemExit(f"[{label}] Home-only part still present: {left}")
    if "\u2014" in s or "\u2013" in s:
        raise SystemExit(f"[{label}] dash found")
    if lang == "ar":
        s = keep_names_together(s)
    return s


def main():
    en_src = (ROOT / "en" / "index.html").read_text(encoding="utf-8")
    ar_src = (ROOT / "index.html").read_text(encoding="utf-8")
    tags = re.findall(r"breadcrumbs\.js\?v=(\w+)", (ROOT / "en" / "speakers.html").read_text(encoding="utf-8"))
    if len(set(tags)) != 1:
        raise SystemExit("breadcrumbs.js tag not found in en/speakers.html")
    bc_tag = tags[0]
    for sp in SPEAKERS:
        for lang, src, out in [
            ("en", en_src, ROOT / "en" / f"speaker-{sp['slug']}.html"),
            ("ar", ar_src, ROOT / f"speaker-{sp['slug']}.html"),
        ]:
            text = build(sp, lang, src, bc_tag)
            out.write_text(text, encoding="utf-8")
            print("wrote", out, len(text), "bytes")


if __name__ == "__main__":
    main()
