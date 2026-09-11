#!/usr/bin/env python3
"""Tags and pull quotes supplied by the user, transcribed from the spreadsheet.

Keyed by a distinctive phrase from the episode title. The mapping to slugs is
done by matching that phrase against episode-meta.json, and every row must match
exactly one episode or the run aborts: attaching a quote to the wrong episode is
the same class of error as the Stiegler/Pavlousek mix-up and is not acceptable.

Rows the sheet itself flags as having had the wrong transcript fed to them are
listed in SUSPECT and are verified against the real transcript before use.
"""

SUSPECT = {
    "Consequence Over Probability",
    "RAST Inventor",
    "Silent Mind In Screaming Winds",
    "Urs Haari: The Real Truth",
    "Meteorology 101",
}

ROWS = {
"Insights From The Gaggle": (
 "paragliding, safety, CIVL, death, competition, culture, FAI, risk management",
 "It's not one single mistake that leads to a catastrophe. It is a series of combination of errors"),
"Pal Takats on Challenges": (
 "safety, risk-taking, competition, paragliding culture, accountability, innovation, governance, pilot advocacy",
 "It shouldn't be about who is willing to take more risk. It should be always about who is the best pilot."),
"CIVLRESIGN": (
 "civl, resignation, institution, safety, accident, pilot, paragliding",
 "Resignation doesn't mean you quit forever. It's acknowledging and being responsible when things go wrong"),
"Anatomy of a Dream": (
 "paragliding, mountaineering, mind, competition, x-alps, risk, skills, training, mental coach, self-confidence",
 "You take risks because you have the feeling your skills and your experience are enough to keep you alive. And this feeling is really amazing"),
"Demystifying The Science": (
 "parakites, paragliders, dune rider, kite risers, reflex, collapses, speed, glide",
 "I think the biggest problem in parakiting is that people can get so confident that they think they can always fly in all kinds of conditions and start to push the limits. And then at some point, yeah, there is a limit and then it gets really nasty"),
"Legacy and Lifetimes": (
 "paragliders, boomerang, wave leading edge, two-liner, competition, safety, R&D",
 "Flying is like my life. So it doesn't really see the differences from the beginning to today"),
"Maxime Pinot": (
 "paragliding, ground handling, competition, limits, fatigue, hydration, intuition",
 "Our paragliders have limits. The pilots have limits. So at some point, there is no point to fly in some condition with these paragliders"),
"Understanding Skymate": (
 "skymate, harness, paragliding, sensors, autorotation, safety, data, artificial intelligence",
 "We are finally entering an era of something that we can proudly call as smart harnesses, and this is the equipment that can not only sense and anticipate but most importantly it can even react as and when needed"),
"Science Backed Pre Flight Rituals": (
 "mental clarity, cortisol, hydration, light exposure, visualization, pre-flight routine, paragliding",
 "Our goal is to simulate the brain chemistry and the conditions of this sharp morning so that be it 10 a.m. or be it 3 p.m., our mind is clear, focused, and emotionally ready to make it count."),
"Resilience Equation": (
 "hike and fly, world record, x-alps, physical form, mental game, safety, siv, acro",
 "Just keep the joy of flying. Just keep that spark up, you know, don't force it and make it work"),
"Mastering the Unknown": (
 "neuroplasticity, amygdala, mindfulness, visualization, training, flow state",
 "Between stimulus and response, there is a space. And in that space is our power to choose our response"),
"Consequence Over Probability": (
 "risk management, fear, capacity, consequence, paragliding, safety, decision-making, environment",
 "It's not about overcoming your fear. It's about embracing it, figuring out what's going on and then making yourself actually strong. You're an idiot if you're not afraid"),
"RAST Inventor": (
 "paragliding innovation, two-liner safety, EN B class, RAST system, Leeloo X, collapse prevention, aerodynamics",
 "Safety and happy pilots must be always the first step. Business is the second step"),
"Silent Mind In Screaming Winds": (
 "mindfulness, breathing, flow state, mental clarity, self-awareness",
 "If you can recognize yourself going off, then it's really about focusing on the breath, trying to bring yourself into that state where your mind becomes still"),
"Urs Haari: The Real Truth": (
 "reserve parachute, safety training, muscle memory, emergency procedures, unconscious reaction, survival skills",
 "Your body should know where the handle is, of your reserve parachute. With closed eyes, without thinking, those procedures, they need to be in your blood, in your memory, in your cells, in your unconscious"),
"Meteorology 101": (
 "weather forecasting, models, local knowledge, paragliding, meteorology",
 "No matter what the forecasts are saying, no matter what you're seeing, there is one thing that forecasts are not good at, and that's taking into account local knowledge"),
"Road to X-Alps": (
 "paragliding, x-alps, adventure flying, hike and fly, mountains, mental approach, bivvy flying, karakorams",
 "They say in paragliding, you need a little bit of luck, but why is it the same pilots who get lucky every single time?"),
"777": (
 "paragliding, winglets, design, competition, certification, innovation, performance, safety",
 "It's not about the wing, it's about the pilot. The best technology won't save you if you don't have the skills to handle it."),
"Sandrine Roy": (
 "vol-biv, paragliding, adventure travel, sustainability, self-powered journey, hiking and flying, minimalism, freedom",
 "It's not a vacation or holiday. It's life. You have to assume that you are not at your home. You're far. You will not be there for marriage. You will not be there for seeing the kids of your friends"),
"Alain Zoller": (
 "certification, paragliding, safety, test house, collapse, harness, reserve, wg6",
 "We don't focus too much on the collapses because when you collapse the glider, it is absolutely not representative of what you will get in air"),
"Ziad Bassil": (
 "paragliding, wings, test flying, glider reviews, certification, two-liner gliders, lightweight fabrics, harnesses",
 "We are flying to have pleasure. Don't push yourself getting higher rated gliders just to prove. You don't have nothing to prove. You just want to smile. That's enough for everyone and for yourself"),
"Storytime": (
 "paragliding, adventure, risk, john silvester, rescue, bir, ozone, hike and fly",
 "A good pilot should stay within his risk management strategy. Certainly if he's a tandem pilot anyway. But he was a comp pilot, so he'd come from that camping background where it was all about achieving the goal"),
"Ashutosh Chopra": (
 "aviation, paragliding, fear, passion, fighter pilot, g-forces, support system, adversity",
 "You don't want that thing that was a small bit of fear now turn its head and turn into a monster. And which it will. It becomes such a mental block that it's impossible to get out of. So the faster it's handled, the better"),
"Kinga Masztalerz": (
 "paragliding, mental game, honesty, adventure, flying conditions, comfort zone, new zealand, backcountry",
 "Be honest with yourself and truly honest no matter how uncomfortable it may be. And whatever comes out of it, just follow it and you can't go wrong"),
"Helmut Schrempf": (
 "paragliding, siv training, wing control, safety pilot coaching, collapses, maneuvers, harness, two-liners",
 "The wing doesn't have to learn it, the wing already knows. It's more the connection from the pilot to the harness. This is the basic of safety pilot coaching"),
"Marko Milutinovic": (
 "mid-air collisions, competitive paragliding, safety, reserves, gaggle, steerable reserve, competition pilots, flight incidents",
 "The brain is perceiving things differently, so you see every little detail, everything around you, because of the situation you're in"),
"Frantisek Pavlousek": (
 "paraglider design, certification norms, fabric technology, collapse behavior, two-liner wings, line materials, safety vs performance, EN/DHV categories",
 "Every glider is a compromise. The more you push for performance, the more you lose safety"),
"Andreas Lattner": (
 "paragliding, camper van, storytelling, mountaineering, adventure, hochzwei media, risk aversion, 8000ers",
 "If you go to an office from nine to five, you won't be open in your mind for jobs like this. They won't come to you because you have no time for them"),
"Benjamin Kellet": (
 "paragliding, content creation, social media, videography, storytelling, risk management, community growth, brand partnerships",
 "I'm doing this because I love flying. You have to find a balance between capturing the moment and enjoying the experience"),
"Gabriel Orsini": (
 "reserve deployment, safety training, risk vs reward, paragliding equipment, acro flying, instructor ethics, manufacturer accountability, close calls",
 "The number of people who've died on acrobase setups I personally believe exceeds the number of people that the acrobase harness has saved"),
"Christian Ciech": (
 "helmet safety, paragliding, certification, free flight, impact protection, visor, full-face helmet, EN966",
 "The five-year replacement of the helmet is not mandatory. If you keep your helmet in a very good condition, you don't let the helmet fall on the ground, you don't have any crash, then you can keep the helmet longer"),
"Risk Vs Reward 4": (
 "acro paragliding, risk management, competition flying, flight safety, innovation in aviation, teamwork, mental preparation, equipment evolution",
 "If I don't try a new thing because I'm scared, my evolution is stopped. It's only a question of fear that you need to try, and for me, I always try. That's how we crossed many limits"),
"Eric Roussel": (
 "paragliding, manufacturing, innovation, safety, koroyd, harness, design, france",
 "The problem with Koroyd is that you can see what happens when you crash. With other protections, foam or airbags, you can't see if they worked. That's why people talk about Koroyd more: because the evidence is visible"),
"Carabiner Fatigue": (
 "carabiners, material fatigue, paragliding safety, equipment maintenance, dynamic loads, corrosion, microscopic cracks",
 "Each stress cycle, even if it's below the carabiner's maximum rating, adds up over time. And this cumulative effect can weaken the carabiner, eventually making it more susceptible to failing"),
"Flying & Filming 1": (
 "paragliding, storytelling, narrative, sponsorship, filmmaking, monarch butterfly, content creation",
 "I feel like the key to so many of the things that I've done being as successful as they were is that somehow finding a way to really make people care about it"),
"Living The Dream": (
 "paragliding, world records, adventure, dreams, mindset, challenges, visualization",
 "When people do something that they love versus doing something that they don't love, it is said that they are around 10 times more effective"),
"Manfred Ruhmer": (
 "hang gliding, paragliding, competition, risk, safety, technology, instructor, experience",
 "When we fly in extreme conditions, that's when you have to know, am I pushing my limits or the machine's limits? That's where experience speaks"),
"Subir Sidhu": (
 "paragliding, risk, reward, progression, mentorship, safety, adventure, acro flying",
 "Performance doesn't come from the wing. Performance comes from the expertise of the pilot. And the more you invest in your own expertise, the better your performance will become"),
"Philipp Zellner": (
 "paragliding, risk, reward, adventure, himalayas, mentors, safety, acro flying",
 "If you try to chase it too much, it will not come. It will only come when you take it easy"),
"Veselin Ovcharov": (
 "harness, paragliding, safety, innovation, acro, technology, community, fly the earth",
 "We've basically been flying rucksacks for decades, in this amazing sport that deserves so much more. But the technology just drifts the other way"),
"Stephan Stiegler": (
 "paragliding, design, certification, performance, safety, two-line glider, innovation, winglets",
 "It's not always thinking in boxes. It's more like, okay, you have to be open-minded all the time, get input, and not try to follow everybody or anything. Just go your own way"),
"Guillem Batlle": (
 "paragliding, r&d, technology, orikami, harness, aerodynamics, safety, homologation",
 "The more streamlined the flow, the lower the drag yielded by the pilot. And since performance is very important, it's really a good approach"),
"New Technologies 1": (
 "paragliding, speed flying, new technologies, certification, collapse stability, comfort zone, flare system, moustache wing",
 "I think in the future, the brands will start making wings that are more collapse stable, that are safer and focus less on the performance. I think that's what our market needs"),
"Klaudia Bulgakow": (
 "paragliding, competition, mentorship, safety, intuition, women in sports, risk management, career transition",
 "What is the takeaway? Put the hard work in, but listen to intuition. If your intuition says something, you probably should listen"),
"PWCA: Goran": (
 "paragliding, world cup, competition, safety, licenses, standardization, pilots, fai",
 "In paragliding comps, and especially in the World Cup, the only real safety measure is the pilot quality. That's it"),
"Nikolay Yotov": (
 "paragliding, kenya, africa, competition, adventure, wildlife, ethiopia, cross-country flying",
 "Africa is a guarantee for adventure. It's poor, but it's generous. It gives you a lot, especially if you don't come with bad thoughts like, let's consume, let's steal, let's take. It's constant giving and taking"),
"Vistasp Kharas": (
 "paragliding, panchgani, competition, volcanic plateau, wind shear, india, safety, en b gliders",
 "So if you get below 1800 meters, start looking for a safe landing. Don't get close to the terrain unless you really know what you're doing"),
"Godfrey Wenness": (
 "paragliding, mount borah, cross-country, weather conditions, dust devil, kangaroo, world record, australia",
 "If there's one thing that I think every single pilot on this planet will unanimously agree on, it's that when we get into the sport of paragliding, the allure of the sky is so compelling that almost every one of us dreams of turning it into a way of life"),
"Honorin Hamard": (
 "paragliding, competition, world record, training, thermals, glider, french team, cross-country",
 "It's not because you have a better glider that you will do better flights. There are a lot of EN B and EN C gliders which are more than enough to do big flights. You can already do, even with an EN A, more than 200 kilometres in the Alps"),
"Antoine Girard": (
 "paragliding, altitude, expedition, mountaineering, himalayas, world record, oxygen, acclimatization",
 "The most important is to have fun. If you have a lot of fun, for sure you will do some big things"),
"Jigish Gohil": (
 "paragliding, india, bir billing, himalayas, flight safety, paragliding community, back ridge flying, adventure",
 "The link which I mentioned has safety information. That is the must-read thing before anybody comes to Bir. They should know how to keep themselves safe and how to enjoy flying over here safely"),
"Navigating India: Eddie Colfox": (
 "himalayas, paragliding, bir, climate change, safety, navigation, back ridge, front ridge",
 "The most important thing is to survive the day. It's not to go as far as you can. It's to be able to do it again tomorrow"),
"Navigating Colombia": (
 "colombia, paragliding, roldanillo, thermals, cross-country, safety, tourism",
 "Colombia: the only danger is wanting to stay"),
}

# Guest names the spreadsheet reveals that episode-meta did not have.
GUESTS = {
    "Silent Mind In Screaming Winds": "Grant Smith",
    "Understanding Skymate": "Roman Barthelemy",
}
