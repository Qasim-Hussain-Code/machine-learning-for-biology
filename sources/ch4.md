<!-- Day 40 -->

Machine Learning for Biology | Day 40
Chapter 4 begins

There is a reason Chapter 3 ended on random forests.

Averaging many trees is one way to reduce error. Building trees one at a time, each one correcting what the last one got wrong, is another.

Chapter 4 is gradient boosting. Next on the list from Day 12. It already made a quiet appearance in Chapter 3, as a comparison.

The question changes too.

Every chapter so far has been a yes or no. Resistant or not. Bound or not. Named the same or not.

Chapter 4 asks a harder kind of question. Not whether something happens, but when. Some patients in the data are still alive when the study ends. For them the honest answer is not yet, not never.

That is called censoring, and handling it badly is an easy, common mistake.

The data is cancer survival. Real patients, real follow-up time, real recurrence.

Same rigour. Same corrections when I get it wrong. A new kind of question, and a new way for the label itself to lie to you.

<!-- Day 41 -->

Machine Learning for Biology | Day 41
Chapter 4: What Happens to the Patients Who Are Still Alive?

Half these patients are still alive when the study ends.

That is not missing data. It is not a problem to clean up before modelling starts. It is the central fact of this chapter. Model around it carelessly and every number after this post is wrong.

Here is the shape of it.

A patient enrols. Years pass. The study closes on a fixed date, for everyone. It does not matter where each patient's disease happens to be on that day.

Some patients had their event. Recurrence, confirmed, dated.

Some did not, and are alive and disease-free when the clock stops. For them, the true answer is not zero. It is not yet.

Treat that second group as a no. Same as someone followed for ten years who never recurred. You have quietly told the model something false. Followed for eight months with no event yet. Followed for eight years with no event ever. Treated the same, they look identical.

Those are not the same fact. One is early. One is settled.

This is called censoring, and it is not unique to cancer data. Any study with a fixed end date and an event that might happen later has it. Component failure. Customer churn. Reoffending after release.

Biology just makes the stakes obvious.

The wrong move is common, and I want to name it before I am tempted by it. Drop everyone still alive at the end. Keep only patients with a known event.

That feels safe. It is not.

It deletes exactly the patients who are doing best, because good outcomes take longer to prove than bad ones. The remaining data is quietly enriched for recurrence, and the model learns a population that does not exist.

So the label for this chapter is not recur or not. It is two numbers together. How long a patient was followed, and whether the thing being watched for happened before the watching stopped.

Tomorrow: the exact rule, in writing, before a single row is touched.

<!-- Day 42 -->

Machine Learning for Biology | Day 42
Chapter 4: What Happens to the Patients Who Are Still Alive?

Here is the rule, written down before I have loaded a single row.

The event is disease-free survival. Not overall survival, not progression-free survival on treatment. This one specific definition: time from diagnosis to the first confirmed recurrence, or death from any cause, whichever comes first.

Death from any cause is in there deliberately. A patient who dies in a car accident before their cancer could recur is a hard case. Different studies handle it differently. I am counting it as an event, not a censor. Pretending that patient's follow-up simply continued would be its own quiet lie. Recorded now, so I cannot quietly change it later if the number looks better the other way.

Follow-up time is measured from diagnosis, not from enrolment, not from the end of primary treatment. Three different clocks, three different chapters.

Censoring applies to anyone with no confirmed event by their last recorded contact. That includes patients still in active follow-up and patients lost to follow-up. Both get the same treatment: alive and event-free, as of the last date anyone checked.

One threshold, decided now. Patients with less than thirty days of follow-up are excluded before the split, not after. Too little time to say anything, and including them would let the model learn from noise dressed up as signal.

The split is grouped, as it was in Chapter 3. One patient, one group, never divided between train and test. That part does not need deciding. It needs restating, because getting it wrong once already cost a chapter.

Two more decisions, named now so they cannot be adjusted after seeing a result.

The metric is concordance index, not accuracy, not F1. C-index asks a narrower question. Of two randomly chosen patients, does the model rank them in the correct order by risk. Chance is 0.5. A perfect ranking is 1.0.

And the comparison this model has to beat is not zero. It is stage alone. Whatever a clinician already knows from TNM staging, unaided, on the same patients. If gradient boosting cannot beat stage, the honest chapter is the one that says so.

Nothing has run yet. The pipeline goes in tomorrow.

<!-- Day 43 -->

Machine Learning for Biology | Day 43
Chapter 4: What Happens to the Patients Who Are Still Alive?

I do not know yet whether this chapter will work. Here is why it might not, written before I find out.

Public cancer cohorts are not a random sample of cancer patients. They are the patients whose data made it into a study. At institutions with the funding to run one. Filtered by inclusion criteria that already excluded the sickest and most complicated cases.

Whatever this model learns, it learned from that population. Not from cancer patients generally.

Second problem, and this one is structural rather than a sampling issue. Stage, grade, and tumour size are correlated with each other by construction. Bigger tumours tend to be later stage. Later stage tends to mean higher grade. A model can look like it found three independent signals. It may have found one signal, badly, three times.

Chapter 3 had a name for this. Circularity. A model detecting the tool that made the label, not the biology underneath it. The version here is one clinical fact, detected through three correlated proxies, reported as three important features instead of one.

Third. Small event count. If confirmed recurrences in this cohort number in the low hundreds, the honest ceiling is lower than the sample size suggests. Survival models are limited by how many events occurred, not by how many patients were enrolled. A cohort of a thousand patients with sixty events behaves, for fitting purposes, much closer to a cohort of sixty.

Fourth, and this is the one I am most likely to get away with unless I check for it directly. Follow-up time itself can carry information that has nothing to do with biology. Some patients are followed more closely because a clinician was already worried. That worry, not the tumour, can end up predicting outcome.

None of these break the chapter. Each one changes what a result would mean. Each one gets checked and reported, whether or not it changes the headline number.

Tomorrow: the model itself, and why gradient boosting needed a different objective function for this.

<!-- Day 44 -->

Machine Learning for Biology | Day 44
Chapter 4: What Happens to the Patients Who Are Still Alive?

Every model in this series so far has been trained to predict one number and check it against one answer.

This one predicts a number and gets checked against two things at once. Whether the event happened, and how long it took.

Ordinary gradient boosting cannot do that. It needs an objective function that understands censoring, or it will do exactly what Day 41 warned about. Score a patient still doing well at eight months the same as one confirmed disease-free at eight years.

The fix is called the Cox partial likelihood, and the idea behind it is older than gradient boosting itself.

Do not ask the model to predict a survival time directly. Ask it to predict a risk score. Judge that score only by whether it puts patients in the right order.

Here is what that means in practice. At the moment each event occurs, look at everyone still at risk. The patient it happened to should have scored higher risk than everyone else still in the running at that moment.

Do that at every event in the data and add it up. That is a single number the model can be trained to improve. The model is never asked to know exactly when. It is asked to know who is more at risk than whom, at every moment someone's risk became real.

That is why the metric from Day 42 is concordance, not accuracy. The model was trained to get orderings right. It gets scored the same way.

One consequence worth sitting with before any result exists. A model can have excellent concordance and still be useless for telling one specific patient how long they have. Ranking who is higher risk is a different skill from predicting a date.

This chapter is about the first skill. Naming that limit now, not after a number makes it inconvenient to say.

Pipeline runs next. First numbers, honestly, whatever they are.

<!-- Day 45 -->

Machine Learning for Biology | Day 45
Chapter 4: What Happens to the Patients Who Are Still Alive?

The pipeline ran. Here is what it found.

586 patients, from two public colorectal cancer datasets. 185 of them had something happen: the cancer came back, or the patient died. The other 401 had not, as of the last time anyone checked on them.

That second group matters. They are not "no event." They are "not yet."

I built a model, using a family of methods called gradient boosting, and gave it ten pieces of information about each patient: things like cancer stage, lymph node status, and treatment history. Its job was to rank patients by risk, not to predict an exact date.

I tested it on 176 patients the model had never seen, 56 of whom had an event. The model scored 0.7289 on a measure called the concordance index, which works like this: pick two random patients, and ask whether the model correctly guessed which one was at higher risk. A score of 0.5 means pure guessing. A score of 1.0 means always right. 0.7289 means the model got the ordering right about seventy-three times out of a hundred.

For comparison, I also scored the simplest possible baseline: cancer stage alone, the number a doctor already has before any model is involved. Stage alone scored 0.6743 on the same patients.

Two checks I promised to run, before I knew what they would show:

1st: what if I only look at colon cancer, leaving out rectal cancer? On colon cases alone, the model scored 0.7228 against 0.706 for stage. Still an improvement, but a smaller one, and this time the gap is not clearly bigger than what chance alone could produce. Both groups agree the model does better. Only the larger, mixed group is confident enough to say that improvement is real rather than noise.

2nd: does knowing how many mutations a tumour carries add anything? 540 of the 586 patients had this data available, and the pattern in the numbers matched what is already known about this type of cancer, so I trust the measurement. Adding it changed the score by less than one point, and that tiny change could easily be nothing at all. My honest conclusion: mutation count did not help this model predict risk.

Before running any of this, I named two specific worries out loud.

Worry one: what if patients who are checked on more often, because a doctor is more concerned about them, get a worse score just from being watched more closely, rather than from anything about their actual cancer? It did not happen. 

Worry two: what if the model finds one real signal, but reports it as two or three separate important features, making it look like it is using more information than it actually is? This one happened. 

What this chapter actually shows:

The model ranks patients by cancer risk somewhat better than stage alone does.

Code: [link to the chapter repository]
