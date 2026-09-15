# -*- coding: utf-8 -*-
"""Gizlenmis Ingilizce AI ornekleri — parti 4.

Bu partide uslup cesitliligi kasitli olarak genisletildi: onceki iki parti
agirlikli olarak sakin/gozlemci birinci sahis anlatiydi. Model tek bir
"gizlenmis AI sesi" ogrenmesin diye burada sinirli, kararsiz, teknik,
listeye kayan ve yarida kesilen kayitlar da var.
"""

SAMPLES = [
"""Right, so the boiler. Third time this winter.

Engineer came out Thursday, said it was the pressure valve, topped it up, charged me nothing because it's still under the contract. Fine. Sunday morning it's down again and the heating's off and I'm standing in the kitchen in a coat at seven in the morning reading a manual I've read twice before.

The manual has a troubleshooting section that ends, and I'm quoting, "if the problem persists, contact a qualified engineer." Thanks. That's where I started.

What gets me is that the engineer clearly knew it would come back. He said "if it goes again, ring us" in a tone that wasn't hypothetical. So there's a diagnosis he either can't make or isn't authorised to make, and the system is going to repeat this until something fails properly enough to justify replacing it.

I've booked another visit. Tuesday afternoon. I'll be taking the afternoon off work, which is the part nobody puts a price on.""",

"""Things I have learned about moving house, having done it on Saturday:

Boxes are heavier than the objects inside them, which makes no sense but is consistently true. The kitchen takes four times longer than you plan for. Books should go in small boxes and you will not do this.

Nobody tells you that the worst part is the last hour, when what remains is everything that didn't fit a category — the cables, the single glove, the charger for something you no longer own. By that point you've stopped sorting and you're just putting things in bags.

The new place echoes. I'd forgotten that empty rooms sound different, and that furniture is partly an acoustic decision.

I have not found the kettle. I know it was packed because I packed it. Three days now, tea made in a saucepan, which works fine and which I resent every time.

Two of the boxes are labelled "misc." Past me is not a helpful colleague.""",

"""I don't think I like my hobby any more and I'm trying to be honest about it rather than just quietly stopping.

I've been running for six years. Started after a bad winter, kept going, did two half marathons, the whole arc. For most of that it was the thing that made the rest of the week work.

Sometime last spring it turned into an obligation. I still go. The times are roughly the same. But the part where it cleared my head has gone, and now it's forty minutes of counting down.

The obvious answer is to stop, or change something — different route, different distance, run with someone. I've tried the route thing. It didn't help, which worries me more than the original problem, because it suggests the issue isn't the running.

I've not told anyone this. It seems like a small thing to need to say out loud, and also I suspect saying it would make it real in a way I'm not ready for.""",

"""Can anyone explain why the train company sends a delay notification twelve minutes after the delay has resolved itself?

Genuine question. This morning: 7:42 service, running normally, boarded fine, sat down. At 7:54, while moving at what I'd call full speed, my phone tells me the 7:42 is delayed by eight minutes. It wasn't. It left on time. I was on it.

This has happened often enough that I've stopped trusting the alerts entirely, which is the opposite of the intended outcome. The one time I actually needed the information — proper cancellation, replacement bus — the notification arrived after I was already on the platform looking at a board.

Someone will say it's automated from a data feed with a lag. Fine, I believe that. But the lag makes it worse than nothing, and nothing would be free.

Anyway. Not a complaint exactly. More of an observation about systems that are technically functioning.""",

"""My sister and I have completely different memories of the same holiday and neither of us is lying.

Summer, mid-nineties, a cottage in Wales with a wood burner. She remembers rain for nine days and being bored to the point of tears. I remember a beach, a specific afternoon with a kite, and being happy in an uncomplicated way I can still half-feel.

We've compared details. The cottage is the same. The car journey is the same, including a specific argument about a map. But her version has our father absent for most of it — work, apparently — and in mine he's there throughout.

Our mother, consulted, sided with my sister on the rain and with me on our father, and then said she remembered it as being in August when we both thought it was July.

I've stopped trying to resolve it. What unsettles me slightly is that my version feels exactly as solid as it did before I knew it was contested.""",

"""Update on the sourdough situation, since two people asked.

It's alive. It took eleven days rather than the seven the internet promised, and for about four of those I was convinced it had died and was continuing purely out of stubbornness.

Loaf one: flat, dense, edible in the way that a thing can be edible without anyone wanting it. Loaf two: better rise, but I scored it wrong and it split down the side in a way that looked like an injury. Loaf three, yesterday: actually good. Proper crust, open crumb, the whole thing.

I have no idea what I did differently on the third one. That's the honest answer. Same flour, same timings, same oven. Possibly the kitchen was warmer.

This is the part nobody mentions — that the variable you can't control is the one that matters, and you only find out by accumulating enough attempts to notice a pattern. I'm not sure eleven days and three loaves is enough to notice anything.

Loaf four is proving now.""",

"""Small thing but it's been bothering me: my building's intercom rings through to a phone number, and that number is my landline, and I do not own a landline.

I've never owned one. When I moved in three years ago the intercom was already configured this way, presumably by a previous tenant, and I assumed I'd sort it out in the first week. I did not.

What this means practically is that deliveries don't reach me. The driver presses my flat number, a phone rings somewhere in a house I've never been to, and nobody answers. The parcel goes back. I've lost maybe a dozen this way before I worked out what was happening.

I now have everything sent to a locker two streets away, which works and which I've come to prefer, and which means I have no functional reason to fix the intercom.

So the wrong phone number will presumably ring in that house forever, or until someone else moves into this flat and is more organised than me.""",

"""I have become the person who complains about headphones on public transport and I don't know when it happened.

Twenty minutes on the bus this morning, a man watching something on speaker. Not loudly, in fairness. But audible, and with that particular tinny quality, and I spent the entire journey composing things I would never say.

The thing is I know exactly why he was doing it. His headphones were probably broken or forgotten. He had twenty minutes and something he wanted to watch. If I'd been in that position five years ago I might have done the same and thought nothing of it.

What changed isn't the behaviour, it's me. Somewhere between then and now I acquired a set of opinions about shared space that I did not consciously adopt and cannot fully justify.

I got off two stops early, which I told myself was for the walk.""",

"""Trying to describe a work problem without naming anything, so this may be vague.

There's a process at my job that everyone agrees is broken. It's been raised in three separate meetings over about eight months. Each time, the outcome is that someone will "look into it," and each time that someone is a different person, and each time the looking-into produces a document that circulates once and is not referred to again.

I've read all three documents. They identify substantially the same problem and propose substantially the same fix. The third one cites the first, which suggests its author knew the history and expected a different result, which is either optimism or something sadder.

Nobody is acting in bad faith. That's the frustrating part. Everyone involved would prefer the process worked. But fixing it would require a decision that crosses two teams, and there's no mechanism for making that kind of decision except a meeting, and meetings produce documents.

I'm told there's a fourth review starting next month.""",

"""Bought a secondhand bike and have spent more on repairs than the bike cost, which I was warned about and ignored.

Eighty pounds, from a man in a garage who described it as "sound." It was, in the sense that all the parts were present. New tyres, new brake cables, a new chain because the old one had stretched past the point where it engaged the gears reliably. Total so far: one hundred and thirty-five.

The frame is good though. That's the thing everyone says and it turns out to be true — the frame is the bit you can't easily replace, and this one is straight and the right size and rides well now that everything attached to it is new.

I've done about ninety miles. At current rates the bike will break even against a monthly bus pass sometime in July, which is the kind of calculation I keep doing and which is obviously not the reason I bought it.

The bell doesn't work. I've decided that's characterful.""",

"""Question for people who've done this: at what point did you stop being nervous about the commute?

New job, forty minutes each way, two changes. It's been three weeks. I still leave fifteen minutes earlier than I need to because I don't yet trust the connections, and I still get a small jolt of anxiety when a train sits at a platform longer than feels normal.

My previous job was an eleven-minute walk for six years, so I'm aware my baseline is unusual.

The colleagues I've asked seem genuinely puzzled by the question. One of them does an hour and ten and described it as "just the day." Another reads. A third said the first month was the worst and then it became invisible, which is encouraging and also slightly unnerving as a description of a third of one's waking hours.

I've started listening to things. It helps. I'd still rather be walking eleven minutes.""",

"""The tree outside my window is coming down next week and I've had a strange few days about it.

It's not a remarkable tree. Sycamore, maybe forty years old, and the council's notice says it's diseased and structurally unsound, which I have no reason to doubt — a branch came off in February and took out a section of fence.

But it's the only thing I can see from my desk that isn't a building. I've watched it through four winters without ever thinking of it as something I was watching. I know roughly when it comes into leaf. I know the specific way the top moves in wind that isn't otherwise noticeable at ground level.

There's no argument here. It's genuinely unsafe and a replacement is being planted eight metres further along, where it won't be visible from this window.

I've taken a photograph, which felt ridiculous while I was doing it and which I'm glad I have.""",
]


def rows():
    return [{"text": " ".join(t.split()), "label": 1, "lang": "en",
             "source": "claude-hard/gizlenmis", "attack": "none"} for t in SAMPLES]


if __name__ == "__main__":
    r = rows()
    ws = sorted(len(x["text"].split()) for x in r)
    print("parti 4: %d ornek | kelime: min %d, medyan %d" % (len(r), ws[0], ws[len(ws)//2]))
