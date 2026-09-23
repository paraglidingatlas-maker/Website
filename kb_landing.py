"""Content for the knowledge base category landing pages (the lighter layout).

generate_kb_pages.category_page() switches a category to kb_layout.landing()
when its slug has an entry here. Each entry needs:
  kicker (the category name), h1 (a pilot's question), lead, sub, seo_title
  (70 characters or fewer), seo_desc (70 to 165), hero_alt, series_heading,
  series_kicker, faq_heading, and faq: five {q, a, src:[(episode, chapter, who)]}.
Hero image: assets/images/kb-<slug>.jpg (2400x900) with a .webp beside it.

Rules, as for the series pages: paraphrase, no dashes, questions end in "?",
answers 55 to 70 words. Everything here comes from the published series pages
(and the chapters they cite), and no question repeats a series page FAQ.
Chapter links are validated at build time, like the series pages.
"""
from kb_editorial import *  # noqa: F401,F403  (episode slug constants)

LANDING = {
    "core-series": {
        "kicker": "Core Series",
        "h1": "How Do Experienced Pilots Travel, Train and Live for Flying?",
        "lead": "Three series about people rather than physics: local pilots on flying their home sites, the pilots at the top of the sport on how they train and think, and pilots who built their lives around flying. Each is written from the episode transcripts, with every claim linked to its chapter.",
        "sub": "This comprehensive collection is divided into three main sections, each designed to inspire, equip, and build your understanding of free flight from the ground up.",
        "seo_title": "Travel, Train and Live to Fly: Core Series | Paragliding Atlas",
        "seo_desc": "Local pilots on their home sites, top racers on how they train and think, and pilots who built a life around flying: the Core Series of the Paragliding Atlas.",
        "hero_alt": "An abstract drawing: faint contour lines of hills with a single pilot's track looping up through thermals and gliding on between them",
        "series_heading": "The three series",
        "series_kicker": "Built from the episodes",
        "faq_heading": "Questions across these series",
        "faq": [
            {"q": "Is it worth hiring a local guide when you fly abroad?",
             "a": "Eddie Colfox thinks so. In his view a pilot with 100 to 300 hours is still a beginner, and with an experienced guide or a group you fly five hours a day instead of two, learn more and are safer. Chris Garcia builds his tours around local pilots for a similar reason: when the weather turns tricky or something goes wrong, locals know best what to do.",
             "src": [(EDDIE, "c4", "Eddie Colfox"), (CG, "c4", "Chris Garcia")]},
            {"q": "Do you need oxygen to paraglide at high altitude?",
             "a": "The guests differ. Antoine Girard recommends oxygen for pilots new to altitude: with less oxygen the brain slows down just as the wing speeds up, and at 8,000 metres a wing trims at about 60 km/h. Damien Lacaze does not carry it: after a week of acclimatisation, sleeping at 4,000 metres and walking higher by day, he finds flying at 6,000 to 6,500 metres fine.",
             "src": [(AG, "c8", "Antoine Girard"), (DL, "c12", "Damien Lacaze")]},
            {"q": "How many hours a year do the best paragliding pilots fly?",
             "a": "A lot. Maxime Pinot says pilots who set out from scratch to reach the World Cup typically fly 400 to 500 hours a year, though experienced pilots can fly less; he has flown between 250 and 450 a year for about 20 years. Honorin Hamard now flies about 500 hours a year, has around 8,000 in total, and flew more than 200 in each of his first years.",
             "src": [(MP, "c4", "Maxime Pinot"), (MP, "c12", "Maxime Pinot"), (HH, "c11", "Honorin Hamard"), (HH, "c2", "Honorin Hamard")]},
            {"q": "Can you make a living from paragliding?",
             "a": "Some of the guests do, in very different ways. Honorin Hamard is now a test pilot. Benjamin Jordan built his career by cutting his living costs to almost nothing for about ten years, in a converted school bus, so he could say yes to projects. Shams turned his dog's unplanned fame online into brand collaborations, and Chris Garcia started a paragliding tour company in 2023.",
             "src": [(HH, "c6", "Honorin Hamard"), (BJ, "c4", "Benjamin Jordan"), (SHAMS, "c9", "Shams"), (CG, "c2", "Chris Garcia")]},
            {"q": "How do experienced pilots decide not to fly?",
             "a": "By setting limits and keeping to them. Maxime Pinot tells the young pilots he trains that if a race would cancel the task, they do not fly. Honorin Hamard abandoned a record attempt after three frontal collapses downwind of a mountain, and went down to try another day. Damien Lacaze warns that in a storm, the moment you want to land is already too late.",
             "src": [(MP, "c7", "Maxime Pinot"), (HH, "c1", "Honorin Hamard"), (DL, "c11", "Damien Lacaze")]},
        ],
    },
    "competitions": {
        "kicker": "Competitions & Performance",
        "h1": "How Do You Race, Judge Risk and Keep a Clear Head in Paragliding?",
        "lead": "Three series for pilots who want to go further: how competitions are set and scored and how pilots climb the ranking, how experienced pilots decide when to push and when to stop, and the mental side of flying, with the tools around it.",
        "sub": "Take a tour into the thrilling world of racing paragliders and learn how to push your performance boundaries safely and effectively. Strategies, training techniques, and mindset from the pilots who have done it all.",
        "seo_title": "Racing, Risk and a Clear Head: Competitions | Paragliding Atlas",
        "seo_desc": "How paragliding competitions are scored, how experienced pilots judge risk and when to stop, and how to stay calm and focused in the air: three series in one place.",
        "hero_alt": "An abstract drawing: competition turnpoint cylinders of different sizes, with an orange optimised route touching the edge of each on its way to a goal line",
        "series_heading": "The three series",
        "series_kicker": "Built from the episodes",
        "faq_heading": "Questions across these series",
        "faq": [
            {"q": "Should you race flat out in your first paragliding competitions?",
             "a": "Not yet, says Joerg Ewald. Fly as far as you can first, because speed comes once the distance game works. Manfred Ruhmer separates the two kinds of risk a race asks you to take: losing the task is one, and flying where the landing options have gone is the other. The first is the sport; the second is the one to design out of your flying.",
             "src": [(GAP, "c12", "Joerg Ewald"), (MANFRED, "c6", "Manfred Ruhmer")]},
            {"q": "Which matters more for safety, SIV or active flying?",
             "a": "Each has its job. Subir Sidhu's point is that you will only recover a shape your glider has been in before, which is what SIV is for, and the earlier the better. Beni Kälin warns that a rehearsed stall does nothing for a big collapse ten metres above the ground: active flying, keeping the wing open in the first place, is the skill that counts there.",
             "src": [(SUBIR, "c8", "Subir Sidhu"), (META, "c9", "Beni Kälin")]},
            {"q": "How do you know when you are pushing too hard?",
             "a": "Start by asking why you are pushing, says Grant Smith: glory is a fine driver, but an accident in an ego battle is a meaningless one. Beni Kälin adds that more flying does not automatically mean more safety, because day after day of smooth air breeds overconfidence. A break makes flying feel fast again, and in his view that feeling is exactly the point.",
             "src": [(GRANT, "c9", "Grant Smith"), (DK, "c1", "Beni Kälin")]},
            {"q": "How should a paraglider be tested before you trust a review?",
             "a": "Where it is hard, says the reviewer Ziad Bassil: low, in turbulent air where you have to push on and turn, not in the strongest conditions or on the best day. That is where a high aspect ratio wing will not turn on a dime and the differences between wings show. He also points out that reflex resists collapse but has nothing to do with trim.",
             "src": [(ZIAD, "c4", "Ziad Bassil"), (ZIAD, "c9", "Ziad Bassil")]},
            {"q": "How do you learn from a flight that went wrong?",
             "a": "Look past the outcome, says Subir Sidhu. If you got away with a bad launch, an incident still happened, so ask what it was, why it happened and whether you knew. Will Gadd is blunt about clouds in particular: nobody gets sucked in, you flew into it. Own that decision, and you can fix it next time by leaving earlier and checking the radar.",
             "src": [(SUBIR, "c8", "Subir Sidhu"), (WILL, "c13", "Will Gadd")]},
        ],
    },
}
