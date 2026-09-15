# -*- coding: utf-8 -*-
"""Gizlenmis Ingilizce AI ornekleri — parti 3."""

SAMPLES = [
"""I bought a plant identification app and it has made every walk worse.

Before, a hedge was a hedge. Now I know that the thing growing along the canal path is Japanese knotweed, which is apparently a legal problem, and that most of what I assumed was ivy is in fact three separate species with strong opinions about each other.

The app is confident about everything, which is part of the trouble. It gave me a ninety-four percent match on something in my own garden that turned out, when I checked with an actual person, to be wrong. Not wrong in an interesting way — wrong by an entire family. The person laughed.

So now I don't trust it, but I also can't stop using it, and I've entered a state where I photograph things and then argue with the result. Yesterday I spent four minutes disputing a fern with my phone.

I preferred the hedge.""",

"""The pub at the end of my road changed hands in February and the new owners have removed the carpet.

I want to be clear that the carpet was awful. It was patterned in a way that suggested it had been chosen to hide things, and it probably was. Nobody who drank there would have defended it on any grounds.

But the room is different now. It's louder, for one — the noise goes straight up off the floorboards and comes back at you — and the effect is that conversations at neighbouring tables have become impossible to ignore. The place has the acoustics of a swimming pool and the lighting of a dentist.

They've also introduced a menu with descriptions on it. The chips are now "triple-cooked." They are the same chips.

I still go. I go slightly less. Nobody has said anything to the new owners, and I suspect nobody will, and in six months this will simply be what the pub is like.""",

"""I have a folder on my desktop called "sort" and it has been there for six years.

It currently contains four hundred and eleven items, including — I checked — three copies of the same tax document, a video of a dog that is not my dog, and a text file called "notes" that opens to a single line reading "ask about the thing."

The folder's function is not storage. It's deferral with a user interface. Anything I can't immediately categorise goes in, and the act of putting it there produces a small feeling of resolution that is entirely unearned.

Twice I've attempted to sort it. Both times I made it through perhaps forty items before creating a subfolder called "sort later," which is the moment the project became self-aware and I stopped.

I know the correct move is to delete it unopened. Six years of evidence suggests nothing in there has ever been needed. And yet.""",

"""My father has developed a habit of forwarding me news articles without comment. Three or four a week, always from the same two sites, always about subjects he knows I have no professional interest in.

For about a year I read them and replied with something. Then I started replying less. He kept sending them at exactly the same rate, which told me the replies had never been load-bearing.

Recently I've begun to suspect the forwarding is not about the articles. It's a small regular signal, the digital equivalent of a wave from across a car park, and the content is incidental — he sends what's in front of him at the time.

Once I tested this by replying with a genuine question about one of them. He answered in two sentences and sent another article the following morning.

I've stopped reading them. I still open them, which I recognise is not the same thing but seems to matter to me for reasons I haven't examined.""",

"""There is a specific sound my car makes when it's cold that three separate mechanics have failed to reproduce.

It happens for roughly the first ninety seconds after starting, below about four degrees, and only if the car has been stationary overnight. By the time I reach a garage it has stopped, and it will not start again until the next cold morning, by which point I am at home and the garage is not.

I recorded it on my phone. The recording is useless — it captures mostly the engine, and the sound in question is quiet and high and, in the recording, indistinguishable from nothing.

The third mechanic suggested I drive it to him at seven in the morning, which is reasonable and which I have not done, because seven in the morning is when I have decided the problem is probably fine.

It's been doing this for two winters. Something is presumably wearing out. I have made peace with discovering what, eventually, at an inconvenient moment.""",

"""A friend asked me to look after her cat for nine days and I have learned that I am not a cat person, which is awkward because I had assumed I was.

The cat is fine. That's the thing — there's no dramatic failure here. It eats, it sleeps in a patch of sun that migrates across the floor, it tolerates me with what I can only describe as professional courtesy.

What I've discovered is that I need animals to want something from me. The cat wants nothing. Food appears whether or not it performs enthusiasm, and it has correctly calculated that enthusiasm is therefore unnecessary. This is rational and I find it faintly insulting.

On day six it sat on my lap for eleven minutes and I felt disproportionately pleased, which I understand is exactly the mechanism the entire species runs on. Knowing this did not reduce the effect.

She comes back Thursday. I'll say it went well, which is true.""",

"""I've been going to the same barber for nine years and I still don't know his name.

This was manageable for the first year or two. By year four it had become a problem I had actively deferred, and at this point asking would require explaining why I hadn't asked earlier, which is a conversation with no good version.

He knows mine. He uses it. He remembers that I once mentioned a trip to Lisbon and asks about it periodically, though the trip was in 2019 and I have not been back.

I've looked for the name in obvious places — the shop sign is just the street name, there's no card, the card machine says the business name which is different again. I could ask another customer. I have considered this seriously, which is probably worse than just asking him.

Nine years is long enough that the not-knowing has become a kind of fact about my life rather than an oversight.""",

"""The supermarket near me reorganised its layout in January and I have not recovered.

I understand why they did it. There's research on this — moving things forces you through aisles you'd otherwise skip, and the resulting purchases more than cover the cost of the disruption. I know I'm the subject of an intervention and I know it's working.

What surprises me is how much of my shopping was automatic. I had no idea I knew where the tinned tomatoes were until I didn't. The knowledge wasn't stored as a fact I could retrieve; it was stored as a movement, and the movement now goes to a shelf of cereal.

My trips take about six minutes longer. I buy, by my estimate, two or three additional items I did not plan. Over a year that's a meaningful sum, extracted from me by furniture.

I've started going to the smaller shop on the corner. It's more expensive. I'm aware this is also a choice they've made for me.""",

"""My upstairs flat has a smoke alarm with a dying battery and the occupants are, apparently, on holiday.

It began chirping on Saturday afternoon. Once every forty seconds, a single high note, entirely regular. It is now Tuesday.

The first day I found it mildly irritating. The second day I found it maddening in a way that felt disproportionate and slightly alarming. By last night I had passed through into something calmer — I hear it, I note it, I continue. I assume this is what people mean by acclimatisation, though I notice it doesn't work when I'm trying to sleep.

I've knocked. I've left a note. I've asked the neighbour opposite, who said she thinks they're in Greece and confirmed that she can hear it too and has adopted the same strategy of endurance.

The battery will die completely at some point. I've caught myself wondering how long that takes and then deciding I'd rather not know, in case the answer is weeks.""",

"""I kept a spreadsheet of everything I read for four years and then stopped, and I've been trying to work out why.

The spreadsheet was thorough. Title, author, dates started and finished, a rating out of ten, and a column called "notes" that was usually empty but occasionally contained something like "too long" or "reread this."

It worked in the sense that I have the data. I can tell you that I read forty-one books in 2021 and that my average rating was 6.8, which is a number I find slightly embarrassing — it suggests I spent a great deal of time on things I thought were fine.

I think the problem was the rating column. It turned reading into assessment. I'd be two hundred pages in and part of my attention would already be composing the score, which is a poor way to be inside a book.

I haven't tracked anything for eighteen months. I also can't tell you what I read last spring, and I don't entirely mind.""",

"""There's a man who sells flowers outside the station and I have never once seen anyone buy from him.

He's there most weekday evenings, roughly five until eight, with three buckets. The stock changes, so presumably something is moving, but in maybe two hundred passes I have not witnessed a single transaction. This has begun to feel statistically improbable rather than merely unlucky.

I've constructed theories. Perhaps the buying happens in a burst I consistently miss. Perhaps the flowers are incidental to some other arrangement, though this is the kind of thought that says more about me than about him. Perhaps people simply don't buy flowers on the way home, and he's been running an unsuccessful business for the four years I've been noticing it.

Last week I nearly bought some, purely to resolve the question, and then realised I'd be doing it for the wrong reason and that I had nowhere to put flowers.

He was there again yesterday. Tulips.""",

"""I did a jigsaw puzzle for the first time since childhood and it took eleven days and I'm not sure I enjoyed it.

A thousand pieces, a photograph of a harbour, bought in a charity shop for two pounds with no guarantee that all the pieces were present — which, it turns out, is a significant thing to gamble on emotionally.

The first two evenings were genuinely absorbing. Edges, then the obvious regions, then the sky, which is where the trouble starts. Four hundred pieces of sky differing by degrees I could not reliably perceive. I sorted them by shape, then by shade, then abandoned systems entirely and simply held pieces against gaps until something fitted.

On day nine I accepted that it was not absorbing any more but that stopping would be worse. That's a different kind of motivation and I don't think it's a good one.

Every piece was there. I felt relief rather than satisfaction, took a photograph nobody wanted, and broke it up the next morning.""",
]


def rows():
    return [{"text": " ".join(t.split()), "label": 1, "lang": "en",
             "source": "claude-hard/gizlenmis", "attack": "none"} for t in SAMPLES]


if __name__ == "__main__":
    r = rows()
    ws = sorted(len(x["text"].split()) for x in r)
    print("parti 3: %d ornek | kelime: min %d, medyan %d" % (len(r), ws[0], ws[len(ws)//2]))
