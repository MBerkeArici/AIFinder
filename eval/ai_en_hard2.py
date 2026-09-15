# -*- coding: utf-8 -*-
"""Gizlenmis Ingilizce AI ornekleri — parti 2.

Bu metinler "insan gibi yaz" talimatiyla uretilmis yapay zeka ciktisini
temsil eder: degisken cumle ritmi, somut ve beklenmedik detay, kalip
ifadeden kacinma, kusurlu/yarim birakilan dusunceler, birinci sahis.

Egitim seti icin insan tarafi `data/human_en_informal.jsonl` (Reddit,
gayriresmi birinci sahis anlatilar) ile eslesir. Bu eslesme sart: insan
tarafi yalnizca haber ve ansiklopedi metni olursa model "yapay zeka"yi
degil "kisisel uslup"u ogrenir.
"""

SAMPLES = [
"""The dishwasher broke on a Tuesday, which I mention because the repair company only does Tuesdays in my postcode, so I had to wait a full week to get back to the day it had already been. There's something almost funny about that if you don't think about it too hard.

I washed everything by hand for eight days. The first two days I felt virtuous. By day four I understood why the dishwasher had been invented, and by day six I had developed a system involving two basins and a specific order of operations that I was, briefly, quite proud of.

The repair man arrived and it was a blocked filter. Nine minutes. He showed me how to clean it, which nobody had ever done, and mentioned that most call-outs are this. I paid seventy pounds for nine minutes and a piece of information I should have had five years ago.

I've cleaned the filter twice since. It takes about four minutes and is genuinely revolting, and I suspect I'll stop doing it by autumn.""",

"""I've been trying to remember the name of a song for three days. Not the whole song — I have the melody, I have roughly eleven words from what I think is the second verse, and I have a very strong sense of the room I was in when I first heard it, which was a kitchen, possibly in 2011.

None of this is searchable. I typed the eleven words into three different places and got nothing, which either means I have the words wrong or the song is more obscure than my confidence suggests. I hummed it at my brother over the phone and he said it sounded like four different things, none of which were right.

The annoying part is that I don't especially want to listen to it. I want to know what it's called. The knowing is the entire objective, which is a strange thing to want badly.

It'll come to me at some useless hour, probably while I'm doing something that makes writing it down inconvenient. That's the usual pattern.""",

"""My upstairs neighbour has started playing the trumpet. Not well, and not at unreasonable hours, which makes the whole thing much harder to complain about.

He's clearly a beginner. There's a particular sequence of notes he attempts every evening around seven, and about one time in five he gets through it cleanly, and when he does there's a pause afterwards that I've started to interpret as satisfaction. I have no evidence for this. I've never met him.

I've caught myself listening for it. Not enjoying it exactly — the failed attempts are genuinely unpleasant — but tracking the progress. Two weeks ago he couldn't finish the sequence at all. Now it's maybe one in five.

I think if I met him I wouldn't mention any of this. It would be strange to explain that I've been quietly monitoring his improvement through a ceiling. But I'd be disappointed if he stopped, which I did not expect and am not entirely comfortable with.""",

"""We got a new coffee machine at work and nobody can operate it. This is not an exaggeration or a joke about technology; there are four buttons and a dial, and the relationship between them appears to be non-deterministic.

The old machine was terrible but comprehensible. You put a thing in, you pressed the thing, coffee came out. It tasted like a warm regret but it was reliable. The new one produces excellent coffee approximately half the time and, the other half, a small amount of hot water and a noise.

Somebody printed instructions and taped them to the wall. The instructions are wrong. I know they're wrong because I followed them exactly and got the noise. Nobody will admit to printing them, so nobody will take them down.

There's a man in accounts who can make it work every time. He won't explain his method. I've watched him and I genuinely cannot see what he does differently. He seems to enjoy this.""",

"""I found a receipt in a coat pocket from a restaurant I have no memory of visiting. March, two years ago. Two main courses, one dessert, a bottle of something. Forty-eight pounds.

Two main courses means I wasn't alone. That's the part I keep returning to. I've gone through a plausible list of people and none of them feel right, and I can't ask anyone without the question sounding either accusatory or concerning.

It's not that the evening was significant. Obviously it wasn't, or I'd remember it. What bothers me is the arithmetic: if a whole evening with another person can vanish this completely, then the number of vanished evenings is presumably large, and most of them left no receipt in a coat.

I put it back in the pocket, which was an odd thing to do. I'm not sure what I expect to happen next time I wear that coat.""",

"""Someone in my building keeps leaving books on the stairs. Not abandoning them — they're arranged, spine out, on the windowsill of the second-floor landing, and they change every week or so.

It started with three paperbacks and a note that said "take one, leave one." The note has since disappeared but the arrangement persists, and people clearly understood the assignment, because the selection now includes things that were definitely not there before. A cookbook. Two thrillers. A quite serious-looking book about Byzantine history that has been there for four months and will, I suspect, remain.

I took a novel in January and did not leave one, which I have felt vaguely bad about since. I've been meaning to correct this. The problem is that the books I'd be willing to give away are the ones nobody would want, and offering them feels worse than the original omission.

The Byzantine history book is still there. Every time I pass it I think: someone believed in that one.""",

"""My mother has started sending me photographs of her garden with no accompanying text. Just the photograph, usually slightly crooked, occasionally with her thumb in the corner.

At first I replied with questions. What's the purple one, is that new, did you move the pot. She answers these, briefly, and then sends another photograph the next day. I've come to understand that the questions are not the point and possibly not welcome.

So now I reply with a short thing. Nice. That looks good. The tall ones have got taller. She doesn't respond to these either. The exchange has settled into something that isn't really a conversation but is clearly serving a purpose.

I mentioned it to my sister, who gets the same photographs and has arrived at the same protocol independently. Neither of us knows when this started or what prompted it.

I've looked at the garden in these pictures more carefully than I ever looked at it in person, which I notice without knowing what to do about.""",

"""The gym I joined in January has sent me eleven emails. I have been four times.

The emails have escalated in tone. The first few were encouraging in a generic way. Around week six they became concerned. The most recent one asked whether everything was okay, which I found briefly touching until I remembered it was automated, at which point I found it slightly insulting.

I keep meaning to cancel. The cancellation process requires visiting in person, which is obviously deliberate, and which has the effect of making me avoid the building entirely — the opposite, presumably, of what the policy intends.

So I'm paying thirty-two pounds a month to not go somewhere, and receiving correspondence about it. If I'd simply gone twice a week since January this would have cost roughly the same and I'd be measurably healthier, which is the kind of arithmetic that's more useful in advance than in retrospect.

I'll cancel in April. I've said this before, but in fairness I've never written it down.""",

"""There's a bus stop near my flat where the timetable has been wrong since I moved in. Not slightly wrong — the route number listed hasn't served that stop in at least three years, according to a man I asked while we were both waiting.

We waited together for eleven minutes, which is long enough to establish that we were both experienced enough to know the timetable was fiction and inexperienced enough to be standing there anyway. He said he'd reported it twice. I said I'd been meaning to.

The bus that does serve the stop arrives roughly every twenty minutes and appears on no printed surface. You learn it or you don't.

I've thought about this since, because it seems like a small, clear example of something larger: the official information is wrong, everyone who uses the system knows it's wrong, the knowledge is transmitted informally, and correcting the official version would help only newcomers, who are precisely the people not present to complain.

Nothing has changed. The timetable is still there.""",

"""I tried to teach myself to juggle over the summer. This was not a considered decision; I read an article about motor learning and bought three balls within the hour, which is roughly how most of my hobbies start.

The article said most people can do a basic three-ball cascade in about fifteen hours of practice. I have done perhaps nine hours and I can do four throws. Four throws is not juggling. Four throws is dropping things in a slightly structured way.

What's interesting — and this is the only thing that has kept me going — is that the improvement is not gradual. Nothing happens for days, and then one afternoon something reorganises and you can suddenly do a thing you could not do that morning. I've read that this is normal and involves consolidation during sleep, which would explain why the good sessions are always the first ones of the day.

The balls are on the shelf. I've not practised in two weeks, which means I've probably lost the fourth throw.""",

"""A colleague retired last month after thirty-one years and the thing I keep thinking about is his desk drawer.

He cleared it on the last afternoon and the contents were: a stapler, an unopened box of business cards with a job title he hadn't held since 2009, four pens, a birthday card from someone whose name I didn't recognise, and a small tin of boiled sweets that had fused into a single object.

That's it. Thirty-one years. He put it all in a carrier bag, which was not full.

I'm not sure why this affected me. It isn't sad exactly — he seemed perfectly content, he has plans involving a boat — but there was something disproportionate about the ratio. All that time, and the physical residue fits in one hand.

I cleared my own drawer the following week, partly out of some impulse I didn't examine. Mine was worse. Mine had four dead batteries and a key to a building I no longer have access to.""",

"""My flatmate labels everything in the fridge. Not aggressively — no capital letters, no warnings — just small pieces of masking tape with her initials and, occasionally, a date.

I've never labelled anything. This creates an imbalance where all unlabelled food is implicitly mine, which works fine until someone else's unlabelled food enters the fridge and the system produces its first ambiguous case. This happened in November with a container of soup that neither of us claimed and neither of us threw away for eleven days.

The soup became a kind of test. I understood that eating it would constitute a claim. She presumably understood the same thing. It sat in the middle shelf accumulating meaning until one of us — I genuinely don't know which — disposed of it while the other was out.

Neither of us mentioned it. The labelling continues. I still don't label anything, and I've started to suspect that this is itself a position I'm taking, though I couldn't say what it is.""",
]


def rows():
    return [{"text": " ".join(t.split()), "label": 1, "lang": "en",
             "source": "claude-hard/gizlenmis", "attack": "none"} for t in SAMPLES]


if __name__ == "__main__":
    r = rows()
    ws = sorted(len(x["text"].split()) for x in r)
    print("parti 2: %d ornek | kelime: min %d, medyan %d" % (len(r), ws[0], ws[len(ws)//2]))
