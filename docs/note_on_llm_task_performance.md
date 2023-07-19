## Competitiveness of LLM for focused tasks

GPT-3 and ChatGPU are recognized as great generalist models. ChatGPT in particular makes possible for non-specialists to access, to use, but also to create AI applications almost on the fly, just with natural prompts, offering conversational capacities never seen before. 

These models and their API make possible to very easily create "AI" services, which explains the current boom of such applications. Are these applications however useful for professional tasks? Are they competitive with current SOTA machine learning application using custom training data?   

The natural-sounding, confident outputs of these models, and the usual "positive" prompts/questions (prompts for which an answer exists) tend to bias the perception of users on the actual task performance capabilities of LLM. Humans have a bias to attribute too much intelligence to machines and to have anthropomorphism interpretation for latent statistical properties of web-scale textual distribution learned by the model (  On this topic, see for instance <https://qoto.org/@twitskeptic/110204902784288127> on over-interpreting GPT-4 cherry pickup memorized answers). 

The majority of studies on task-specific performance report lower accuracy or at best similar accuracy as state-of-the-art smaller fine-tuned models (e.g. BERT), which are much cheaper and faster.

### Life science

- **GPT-3**: In Zero shot and few shot learning scenario, GPT-3 very significantly underperforms on standard tasks in Life Science, see:

<https://arxiv.org/abs/2109.02555>, “GPT-3 Models are Poor Few-Shot Learners in the Biomedical Domain”, Moradi and al., Sep 2021 

*"Although GPT-3 had already achieved near state-of-the-art results in few-shot knowledge transfer on open-domain NLP tasks, it could not perform as effectively as BioBERT, which is orders of magnitude smaller than GPT-3"*

<https://arxiv.org/abs/2203.08410>, “Thinking about GPT-3 In-Context Learning for Biomedical IE? Think Again”, Jiménez Gutiérrez and al., Mar 2022

*“Our results show that GPT-3 still significantly underperforms compared to simply fine-tuning a smaller PLM”*

<https://arxiv.org/abs/2305.16326>, "Large language models in biomedical natural language processing: benchmarks, baselines, and recommendations", Chen and al., May 2023 (and <https://github.com/qingyu-qc/gpt_bionlp_benchmark>)

On GPT 3.5 and GPT-4 performance on biomedical tasks with zero and few-shot approaches, similarly observes that fine-tuned BERT models significantly outperforms GPT-3.5 and GPT-4 on every biomedical tasks:

*"Fine-tuning biomedical pretrained language models continues to be a prominent choice especially for tasks involving information extraction and classification"*

*"we recommend fine-tuning a pre-trained biomedical language model as the default choice for a downstream application, as it should be a strong baseline at the very minimum"*

*"The results show that GPT models, especially GPT-3.5, had extremely poor performance in named entity recognition compared to other tasks."*

### General NLP tasks

- **ChatGPT**: for recent surveys see:

<https://arxiv.org/abs/2302.10724>, “ChatGPT: Jack of all trades, master of none”, Kocoń and al., Feb 2023  

*"In this work, we examined ChatGPT's capabilities on 25 diverse analytical NLP. (...) We automated ChatGPT's querying process and analyzed more than 38k responses. Our comparison of its results with available State-of-the-Art (SOTA) solutions showed that the average loss in quality of the ChatGPT model was about 25% for zero-shot and few-shot evaluation."*

<http://opensamizdat.com/posts/chatgpt_survey>, "ChatGPT Survey: Performance on NLP datasets", Matúš Pikuliak, Mar 2023 

*"I conducted a survey of the arXiv pre-prints that compare ChatGPT with other approaches, mainly with smaller fine-tuned models. ChatGPT’s performance is not as impressive as I expected, as it is often outperformed by significantly smaller models."*

This blog details several studies on ChatGPT performance. 

- **GPT-4**: There is currently no clear improvement from GPT-3.5 to GPT-4 reported for task-based applications and more time might be needed for the whole user community to explore the capacities of GPT-4. 

On OpenAI API page: 

*"For many basic tasks, the difference between GPT-4 and GPT-3.5 models is not significant. However, in more complex reasoning situations, GPT-4 is much more capable than any of our previous models."*

The drawback of the fine-tuned specialized "small" transformers such as SciBERT, BioBERT, LinkBERT, etc. is that ML practitioners must train and integrate them in complex data pipelines and services before making them ready to achieving a task. However, once this investment is done, these surveys suggest that LLM might appear uncompetitive and more expensive to operate. 

### One exception

However, we also note one outstanding example of a GPT-3.5 few-shot learning model for a scientific extraction task that significantly surpassed best fine-tuned specialized BERT models (MatBERT). In <https://arxiv.org/abs/2212.05238>, 3 types named entities with relations are extracted from unstructured text in materials chemistry. The learning used in this work involved a high number of training examples for a "few-shot" approach (around 400 training examples were used with the GPT-3.5 davinci model). It shows that this approach could be very effective. As far as we know, this is the only existing work showing a clearly better accuracy for a LLM than a fine-tuned transformer in the scientific literature domain. 

Given the exceptional outcome of this work, it is also not impossible that an error in the evaluation or the methodology took place. 

### Task-related usage

It should also be noted that another possible promising use-case is to use the ability of the model to capture general knowledge and to transfer knowledge to tasks missing training data. Generating synthetic training data is relevant to all ML tasks. For the data type classification task, the less frequent classes, although clearly defined and non-ambiguous, are not supported by enough training examples to be predicted by the fine-tuned SciBERT model. 

For professional applications, ChatGPT and GPT-4 could be used as a quick prototype for some applications, but not as direct competitive enablers as compared to current "BERT" implementations, or possibly as tools to augment the training data.

## Evaluation of LLM

The main issue with current LLM evaluation (when an evaluation is reported!) is test data leaks. It is reported that a significant proportion of evaluation datasets are used as training data in LLM. The [Common Crawl](https://commoncrawl.org) and web data are used at scale for training LLM, including available mainstream evaluation datasets, a problem called contamination. 

The team building [Galactica](https://github.com/paperswithcode/galai) further reported in their paper that they use more or less all available relevant prompts/QA datasets in their training data. Given the importance of these datasets for the “conversational” usability of a LLM, we can expect that, in general, such datasets are used as training data in all modern LLM. Because the current evaluations are focusing on QA applications, LLM are evaluated and compared to a large extend by their ability to memorize seen datasets, more than creating new compositional responses in context.

The same remark has been made for ability of LLM to pass standard medical or law tests. These tests being already available on the web, they are likely well memorized, and we observe that modifying questions, or the wording of some questions, leads to lower performance. 

We need therefore to evaluate our investigations, as much as possible, with fresh evaluation data and recent papers.
