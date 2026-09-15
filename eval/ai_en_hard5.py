# -*- coding: utf-8 -*-
"""Gizlenmis Ingilizce AI ornekleri — parti 5.

Bu partide konu alanlari kasitli olarak dagitildi (is, saglik, para, aile,
teknik ariza, tuketici sikayeti, hatira) ki model konu degil uslup ve
istatistiksel imza ogrensin.
"""

SAMPLES = [
"""Got the results back and everything's fine, which I'm putting first because that's what I'd want to read first.

The three weeks between the scan and the appointment were worse than anything else about it. Not constant — mostly I was fine, working, cooking, normal — but it would arrive at odd moments, usually while doing something mundane, and sit there for a while.

I'd been told the waiting was the hard part by two separate people and had nodded along without understanding. You can't really prepare for it. The uncertainty doesn't respond to reasoning; I could construct the argument that the odds were good and the argument didn't reach the part of me that needed convincing.

The appointment itself took four minutes. The consultant was kind and slightly rushed and I understood roughly half of what she said, and then I was in a corridor.

I've been meaning to write this down for a week. I think I wanted to record that it was survivable, mostly for myself, in case there's a next time.""",

"""The washing machine is making a noise during the spin cycle that I would describe as "grinding, intermittent, worse with heavier loads."

I've looked it up. The internet offers three possibilities: worn drum bearings, something trapped between the drum and the outer tub, or a failing shock absorber. These have wildly different costs — the trapped-object version is free if you can reach it, the bearings version is usually more than the machine is worth.

I've checked the filter. Coin, hair clip, small screw. None of these were causing it; the noise continued.

The machine is nine years old, which is apparently around the average lifespan, so the economically rational move is to replace it. The environmentally defensible move is to repair it. The move I will actually make is to keep using it until it fails completely, which is neither of those things and which I recognise as a decision even though it will feel like an event.

It's on now. You can hear it from the hall.""",

"""My grandfather's watch stopped and I've been carrying it around in my pocket for two weeks without doing anything about it.

It's not valuable. He wore it for maybe thirty years and it was ordinary when he bought it. The strap has been replaced twice, once by him and once by my mother, and the glass has a scratch across the face that predates my memory.

There's a repair place in town. I've walked past it four times. Each time I've had the watch with me and each time I've kept walking, and I've now done this often enough that the not-going has become a thing I'm doing rather than a thing I'm failing to do.

I think what stops me is that it might not be fixable, and at the moment it exists in a state where it might be. That's a stupid reason and I'm aware of it.

It's in my coat now. The repair place shuts at five.""",

"""Six months into the new role and I've worked out that the job I applied for and the job I have share a title and not much else.

This isn't a complaint exactly. The work is interesting and the people are reasonable and I'm paid appropriately. But the description mentioned strategy and what I do is largely coordination, and those are different skills with different satisfactions.

I've raised it once, carefully, in a way that could be read as either a concern or an observation. My manager agreed with the description and did not treat it as a problem, which I've decided was an answer.

What I notice is that I'm good at the coordination. Better than I expected. There's a version of this where I lean into it and in two years I'm someone who coordinates, and that person is doing well and is not the person I intended to become.

I don't know what to do with that. Nothing, probably, for now.""",

"""Ordered a chair online. It arrived in two boxes, one of which contained a different chair.

Not a variant. A completely different product — different colour, different frame, different assembly instructions. The other box had the correct legs and a bag of fixings for the chair I ordered, which means somewhere out there is a person who received the seat I wanted and legs they can't use.

Customer service has been fine, actually. They believed me immediately, which I appreciated more than I expected. But the resolution is that both boxes go back and the order restarts, which is another eleven days and requires me to be present for a collection window I've already rescheduled once.

The wrong chair is in my hallway. I've looked at it quite a lot. It's a perfectly good chair and in another life I might have chosen it, and there's something odd about spending a fortnight with an object that was never meant to be here.

Collection is Thursday. I'll be at work. My neighbour has agreed.""",

"""Trying to eat less meat and finding the social part harder than the food part.

The cooking is fine. I've got maybe eight things I can make that I actually want to eat, which is roughly the same number I had before, and the shopping is cheaper. No complaints there.

What I wasn't ready for is how often it comes up. Every meal with other people involves a small negotiation — either I explain, which makes it a topic, or I don't, which means eating whatever's in front of me and quietly abandoning the whole thing for that evening.

I've mostly gone with the second option, which means the practice is basically domestic. That feels like a failure of nerve, but the alternative is being the person who raises it, and I've met that person.

My brother asked directly last month and I gave a shorter answer than I meant to. He said "fair enough" and moved on, which suggests the difficulty was entirely mine.

Still doing it. About four days a week.""",

"""Two hours trying to get a laptop to see a printer that is eleven feet away and connected to the same network.

The printer works. I know it works because my phone printed to it without being asked, apparently by magic. The laptop can see the network, can see other devices, and denies that the printer exists.

I've reinstalled the driver twice. I've removed and re-added the device. I've restarted everything in a specific order recommended by a forum post from 2019 that had eleven upvotes and gave me more confidence than it should have.

What eventually worked, and I want to be clear that I don't understand why, was assigning the printer a static IP address and adding it manually by that address. The automatic discovery still doesn't work. The printer is now reachable by a route that shouldn't be necessary.

I've written the IP on a sticky note because I know I'll need it again and I know I won't remember. The note is on the laptop. That's the whole system.""",

"""My daughter has started correcting my pronunciation of words she has only read.

She's nine. The words are ones she's encountered in books and never heard aloud — I got "epitome" from her last week, delivered with total confidence as three syllables, and had to decide in about half a second whether this was a moment for accuracy or for letting it go.

I corrected her. Gently. She took it well and then asked why the spelling doesn't tell you, which is a completely reasonable question I could not answer beyond "English."

What struck me afterwards is that I made the same mistakes at roughly the same age with roughly the same words, and that this is apparently what reading ahead of your conversation does. Nobody told me either; I found out at some point by being wrong in front of someone.

She's now suspicious of every long word, which was not the outcome I wanted. I've told her the mistake is a good sign. I'm not sure she believes me.""",

"""Bank sent me a letter about an account I closed in 2018 and I've spent three days establishing that it is genuinely closed.

The letter said my address needed updating for regulatory purposes. Fine, except the account doesn't exist, and saying so to the phone system is not an available option. The menu assumes the account is live. Every branch of the tree leads to somewhere that requires an account number I do not have.

Eventually got through to a person by selecting "opening a new account," which I mention as a tactic. She was helpful and slightly amused. The account is closed. The letter was generated by a separate system that holds historical records and does not check the status field.

She said she'd flag it. She also said, honestly I thought, that flagging it might not stop the letters, because the two systems reconcile quarterly at best.

So I'll probably get another one in March. I now know not to spend three days on it.""",

"""Went back to the town I grew up in for a funeral and stayed two extra days, which I hadn't planned.

The house is still there. Different door, an extension at the back that changes the proportions in a way I found more unsettling than I'd have predicted. I stood across the road for a while, which is a thing I'd previously only seen people do in films and which felt exactly as self-conscious as it looks.

The shop on the corner is a pharmacy. The field behind the school is houses. The school is the same, which surprised me more than the changes — I'd assumed it would have been rebuilt.

What I mainly noticed is how small the distances are. The walk that took twenty minutes takes six. I knew this would be true, everyone says it, and knowing it did nothing to prepare me for the physical sensation of it.

I don't think I'll go back. Not for any strong reason.""",

"""Six weeks of tracking my spending and the results are annoying rather than shocking.

No single disaster. No subscription I'd forgotten, no obvious waste. The problem is entirely distributed: a hundred small transactions that are each individually defensible and which sum to considerably more than I would have estimated.

Lunch is the big one. I knew I bought lunch. I did not know I bought lunch on twenty-three of thirty working days, at an average of eight pounds twenty, which is a number I now can't unknow.

The tracking itself has changed the behaviour, which I'd been warned about and which makes the data slightly useless as a baseline. I've bought lunch four times in the last two weeks. Not because I decided to stop, but because logging it makes it visible, and visible things are harder.

I'll stop tracking at some point and I expect the old pattern to return. Possibly the honest conclusion is that I should just keep tracking forever.""",

"""Neighbour's builders have been here for eleven weeks on what was described to me, in advance and apologetically, as a four-week job.

I want to say clearly that they've been decent about it. The apology was unprompted. They've kept the pavement clear, they start at eight rather than seven, and one of them helped me carry a wardrobe in April without being asked.

But eleven weeks. There's a specific noise — an angle grinder, I think — that happens perhaps twice a day for a few minutes and which I've become so attuned to that I tense up slightly when the compressor starts, because the compressor usually precedes it.

The work itself looks substantial. Foundations were involved. I gather there was something unexpected under the floor, which is apparently the standard reason these things double.

I've not complained and I'm not going to. What I've done instead is develop an unreasonable investment in their progress, and I now find myself hoping they finish for reasons that aren't entirely about the noise.""",
]


def rows():
    return [{"text": " ".join(t.split()), "label": 1, "lang": "en",
             "source": "claude-hard/gizlenmis", "attack": "none"} for t in SAMPLES]


if __name__ == "__main__":
    r = rows()
    ws = sorted(len(x["text"].split()) for x in r)
    print("parti 5: %d ornek | kelime: min %d, medyan %d" % (len(r), ws[0], ws[len(ws)//2]))
