# -*- coding: utf-8 -*-
"""Zor Ingilizce AI ornekleri (bir buyuk dil modeli tarafindan uretildi).

NEDEN: RAID'in AI metinleri siniflandirici icin fazla kolay — 81 ornegin
hicbiri p(AI)<0.8 almiyor, medyan 1.000. Esik bu dagilima gore kalibre
edilince, gercek dunyada iyi yazilmis bir AI metni (olculen ornek: 0.691)
esigin altinda kaliyor ve insan sayiliyor.

Bu set o boslugu doldurur: kalip ifadelerden kacinan, cumle ritmi degisken,
somut detay tasiyan, "AI gibi gorunmemeye" calisan metinler. Olcum setinin
zorluk dagilimini gercege yaklastirmak icin var.
"""

SAMPLES = [
("deneme", """The office plant on my desk has outlived three project managers. It arrived as a housewarming gift when the company moved floors, and nobody has ever claimed responsibility for it. I water it on Fridays, mostly out of habit, and it has responded by growing sideways toward the window in a way that seems faintly accusatory.

There is something instructive in this. The plant requires almost nothing and receives almost nothing, and yet it persists. Meanwhile the elaborate systems we build around our work — the dashboards, the sprint boards, the carefully named channels — require constant attention and collapse the moment someone stops maintaining them.

I am not the first person to notice that neglect is sometimes a form of design. Systems that depend on enthusiasm die when enthusiasm does. Systems that depend on nothing tend to survive, which is why the ugliest spreadsheet in any company is usually the one everyone actually uses.

The plant has no stakeholders. It has never been migrated. When the company changes its tooling again next year, as it will, the plant will simply continue growing sideways, indifferent to the transition plan.

I have started to think of this as a standard worth aiming for. Build the thing that keeps working when nobody is watching it. Everything else is a performance that requires an audience."""),

("analiz", """The economics of remote work are usually discussed in terms of real estate savings, which is the least interesting part of the story. Offices are expensive, but they are a rounding error next to salaries. The real variable is who a company can hire.

When location stops constraining employment, the talent pool expands and the wage floor moves. This cuts in both directions. A firm in an expensive city gains access to candidates who would never have relocated. Those same candidates gain access to salaries their local market could not support. For a period, both sides believe they have won.

The adjustment comes later. Compensation bands, once decoupled from geography, tend to converge downward rather than upward — not through any conspiracy, simply because a company hiring globally has more candidates than positions. The leverage that individual workers briefly enjoyed during the initial shortage does not survive the widening of the pool.

What remains unresolved is the question of tacit knowledge. Organizations transmit a great deal through proximity that nobody has successfully written down: how decisions actually get made, which objections are real, who to ask. Remote firms substitute documentation for this, which works better than skeptics predicted and worse than advocates claim.

The honest summary is that the experiment is still running, and the people running it are also its subjects."""),

("blog", """I spent four hours last weekend trying to fix a dripping tap, and I want to describe what that taught me about estimation.

The repair itself takes about ten minutes. I know this because a plumber eventually did it while I watched. The other three hours and fifty minutes went to: finding out which type of tap I had, discovering that the replacement washer sold in the nearest shop was the wrong size, removing a fixing screw that had corroded into place, and then, at the point where the tap came apart in a way the video had not shown, sitting on the bathroom floor reconsidering several life choices.

None of this was unpredictable in principle. All of it was unpredictable to me, because I had never done it before. That distinction matters more than most estimation advice admits.

We usually talk about estimates as though the problem is optimism. It isn't, quite. The problem is that the work you can see is the work you have done before, and the work you have not done before is invisible until you are inside it. A task is not ten minutes of work plus overhead; it is ten minutes of work surrounded by an unknown quantity of discovering what the task actually is.

The tap no longer drips. I have not attempted the shower."""),

("deneme", """Every few years someone announces that email is dead, and every few years email absorbs the thing that was supposed to replace it. Chat did not kill email; it created a second inbox and then an expectation of immediacy that made the first one worse. Project tools did not kill email; they generate notifications that arrive by email.

The durability is not an accident. Email has three properties its challengers lack: it is federated, so no company can revoke your address; it is asynchronous by default, so a message implies no obligation to answer within minutes; and it is boring, which means it has stopped attracting the kind of investment that produces redesigns nobody asked for.

The complaints about email are largely complaints about volume, and volume is a social problem wearing a technical costume. A tool cannot fix an organization where everyone is copied on everything as a defensive measure. Moving that behavior into a different interface changes its appearance, not its cause.

What has genuinely improved is filtering, though not in the way vendors describe. The useful development was not smarter algorithms but the widespread acceptance that most messages do not require a reply. That is a change in manners, not software.

Email will presumably outlive whatever is announced as its successor next year, for the same reason the fax machine outlived several of its own obituaries."""),

("kisisel", """My grandmother kept a notebook of recipes that is almost useless as a cookbook. The measurements are approximate to the point of hostility — "flour until it feels right" appears twice — and several entries consist of a single ingredient followed by a name, as though the name were the instruction.

I inherited it four years ago and have cooked from it perhaps five times, always badly. The notebook assumes a reader who has stood in the kitchen and watched, which I did as a child without paying the kind of attention that would have been useful later.

What the notebook records is not really the food. It is a set of reminders addressed to someone who already knew how to cook, written in a shorthand that only works if the underlying knowledge is intact. Remove the knowledge and the shorthand becomes decorative.

I have started writing things down differently because of this. Not more thoroughly, exactly, but with more suspicion toward my own sense of what is obvious. The things I would not bother to explain are precisely the things that will be missing later.

The notebook sits on a shelf. I do not use it and will not throw it away, which is its own kind of category."""),

("analiz", """Software estimates fail in a specific and repeatable pattern, and the pattern is informative. Teams are reasonably accurate about tasks they have performed before and wildly inaccurate about everything else, with the error concentrated almost entirely in the second group.

This suggests the problem is not calibration but classification. A team that could reliably sort work into "done this before" and "have not" would produce far better forecasts than one that applies a uniform optimism correction to everything. Most estimation rituals do the opposite: they average across categories and produce a number that is wrong in a different way each time.

The second observation is that estimates degrade with the distance between the estimator and the work. This is unsurprising and yet organizational structures routinely ignore it, gathering forecasts from people whose information is filtered through two summaries.

What actually helps is narrower: shortening the horizon, decomposing until the unknowns become visible, and treating any task that resists decomposition as a research question rather than an engineering one. A task nobody can break down is not a large task. It is an unexamined one.

None of this is novel. It has been written down repeatedly since the 1970s, which raises the more interesting question of why a well-documented failure mode remains standard practice."""),

("blog", """A colleague asked me recently how I decide what to read, and I realized I did not have an answer so much as a set of accumulated reflexes.

The first is that I no longer finish books out of obligation. This took an embarrassing number of years. The sunk cost of a hundred pages feels substantial while you are inside it and evaporates entirely once you put the thing down. I abandon perhaps a third of what I start now, and I read considerably more than I did when I finished everything.

The second is a bias toward older material, not because it is better but because it has been filtered. A book still discussed after forty years has survived a process that no recommendation algorithm replicates. This is not a reliable heuristic — plenty of good work vanishes and plenty of mediocre work persists — but it is cheap, and cheap heuristics are underrated.

The third is that I have stopped trusting my own enthusiasm as a signal. The books that changed how I think were rarely the ones I found exciting at the time; several were mildly irritating. Irritation, it turns out, is often the sensation of an assumption being disturbed, which is closer to learning than agreement is.

The list of things I intend to read remains longer than the list of things I have read. I have made peace with this."""),

("deneme", """There is a particular silence that falls over a meeting when someone asks a question nobody has considered. It lasts about two seconds and it is the most productive moment in the entire hour, which is why it is almost always filled immediately.

Someone will jump in with a partial answer, or redirect to the agenda, or offer to take it offline. All three are ways of ending the discomfort. The question survives only if the person who asked it is senior enough to hold the pause, which means the quality of an organization's thinking is bounded by the seniority of its most curious member.

This is not a small structural problem. The people closest to the work usually notice the inconsistencies first, and they are also the people with the least social permission to stop a meeting. By the time an observation travels upward it has been softened at each step into something that can be said without cost, which is to say into something that does not require anyone to change their mind.

The organizations that handle this well do not have better questions. They have a lower cost of asking them, which is a property of behavior rather than process. No template produces it.

Two seconds is not long. It is long enough."""),

("analiz", """Municipal recycling programs occupy an unusual position in public policy: they are widely supported, moderately effective, and almost universally misunderstood by the people who participate in them.

The misunderstanding is structural. Households are asked to sort material by type, which feels like the substantive contribution, when the economically decisive factor is contamination. A single load spoiled by food residue can render the entire batch unsuitable, meaning the careful sorter and the careless one produce the same outcome when they share a collection route.

This creates an incentive problem that education campaigns address poorly. Telling people to rinse containers is accurate but insufficient, because the benefit of rinsing is invisible and collective while the cost is immediate and individual. Programs that have improved contamination rates have generally done so through collection design rather than persuasion.

The deeper difficulty is that recycling operates downstream of a production system optimized for other properties entirely. Packaging is designed for shelf appeal, transport efficiency, and shelf life; recoverability is at best a tertiary consideration. Asking the disposal end to compensate for decisions made at the design end produces exactly the results one would predict.

This does not make the programs pointless. It does suggest that household behavior is the least leveraged point in the system, which is an awkward conclusion for a policy that depends on household participation."""),

("kisisel", """I ran into a former manager at a train station last month, the kind of encounter where both people have roughly four minutes and no idea how to spend them.

We had not parted badly, exactly, but the project we worked on had gone poorly and neither of us had said much about it at the time. Standing on the platform, he mentioned it directly, which surprised me. He said he had handled it wrong and had thought about it since. I said something about how it had been complicated, which was true and also a way of avoiding the conversation.

His train came first. Afterward I stood there irritated with myself, because he had offered something and I had returned a pleasantry.

What bothers me is that I had rehearsed a version of this conversation for years, and in every rehearsal I was more articulate. The actual version lasted four minutes and I used them badly. The gap between what we intend to say and what we say under mild time pressure is apparently larger than I had assumed.

I have his email. I have not written. I probably will not, and I notice that the reason is not that it would be difficult but that it would require admitting I have thought about it as much as he apparently has."""),
]


def rows():
    return [{"text": " ".join(t.split()), "label": 1, "lang": "en",
             "source": "uretilmis-zor/" + kind, "attack": "none"} for kind, t in SAMPLES]


if __name__ == "__main__":
    r = rows()
    ws = sorted(len(x["text"].split()) for x in r)
    print("zor EN set: %d ornek | kelime: min %d, medyan %d" % (len(r), ws[0], ws[len(ws)//2]))
