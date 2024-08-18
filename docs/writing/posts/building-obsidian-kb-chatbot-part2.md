---
draft: false
date: 2024-08-18
slug: building-obsidian-kb-chatbot
tags:
  - llm
authors:
  - Prabha
---


# Building Personal Chatbot - Part 2

# Enhancing Our Obsidian Chatbot: Advanced RAG Techniques with Langchain

In our [previous post](https://medium.com/@prabhakaran_arivalagan/building-personal-chatbot-with-langchain-ragas-a-journey-of-iteration-and-learning-acbae799124e), we explored building a chatbot for Obsidian notes using Langchain and basic Retrieval-Augmented Generation (RAG) techniques. Today, I am sharing the significant improvements I've made to enhance the chatbot's performance and functionality. These advancements have transformed our chatbot into a more effective and trustworthy tool for navigating my Obsidian knowledge base.

## System Architecture: The Blueprint of Our Enhanced Chatbot

Let's start by looking at our updated system architecture:

![[Pasted image 20240818163253.png]]

This diagram illustrates the flow of our enhanced chatbot, showcasing how each component works together to deliver a seamless user experience. Now, let's dive deeper into each of these components and understand their role in making our chatbot smarter and more efficient.

## Key Improvements: Unlocking New Capabilities

Our journey of improvement focused on four key areas, each addressing a specific challenge in making our chatbot more responsive and context-aware. Let's explore these enhancements and see how they work together to create a more powerful tool.

### 1. MultiQuery Retriever: Casting a Wider Net

Imagine you're trying to find a specific memory in your vast sea of notes. Sometimes, the way you phrase your question might not perfectly match how you wrote it down. That's where our new MultiQuery Retriever comes in – it's like having a team of creative thinkers helping you remember!

```python
self.multiquery_retriever = CustomMultiQueryRetriever.from_llm(
    self.retriever, llm=self.llm, prompt=self.multiquery_retriever_template
)

```

The MultiQuery Retriever is a clever addition that generates multiple variations of your original question. Let's see it in action:

Suppose you ask: "What was that interesting AI paper I read last month?"

Our MultiQuery Retriever might generate these variations:

1. "What artificial intelligence research paper did I review in the previous month?"
2. "Can you find any notes about a fascinating AI study from last month?"
3. "List any machine learning papers I found intriguing about 30 days ago."

By creating these diverse phrasings, we significantly increase our chances of finding the relevant information. Maybe you didn't use the term "AI paper" in your notes, but instead wrote "machine learning study." The MultiQuery Retriever helps bridge these verbal gaps, ensuring we don't miss important information due to slight differences in wording.

This approach is particularly powerful for:

- Complex queries that might be interpreted in multiple ways
- Recalling information when you're not sure about the exact phrasing you used
- Uncovering related information that you might not have thought to ask about directly

The result? A much more robust and forgiving search experience that feels almost intuitive, as if the chatbot truly understands the intent behind your questions, not just the literal words you use.

Now that we've expanded our search capabilities, let's look at how we've improved the chatbot's understanding of time and context.

### 2. SelfQuery Retriever: Your Personal Time-Traveling Assistant

While the MultiQuery Retriever helps us find information across different phrasings, the SelfQuery Retriever adds another dimension to our search capabilities: time. Imagine having a super-smart assistant who not only understands your questions but can also navigate through time in your personal knowledge base. That's essentially what our SelfQuery Retriever does – it's like giving our chatbot a time machine!

```python
self.retriever = CustomSelfQueryRetriever.from_llm(
    llm=self.llm,
    vectorstore=self.pinecone_retriever,
    document_contents=self.__class__.document_content_description,
    metadata_field_info=self.__class__.metadata_field_info,
)

```

The SelfQuery Retriever is a game-changer for handling queries that involve dates. It's particularly useful when you're trying to recall events or information from specific timeframes in your notes. Let's see it in action:

Suppose you ask: "What projects was I excited about in the first week of April 2024?"

Here's what happens behind the scenes:

1. The SelfQuery Retriever analyzes your question and understands that you're looking for:
    - Information about projects
    - Specifically from the first week of April 2024
    - With a positive sentiment ("excited about")
2. It then translates this into a structured query that might look something like this:
    
    ```python
    {
      "query": "projects excited about",
      "filter": "and(gte(date, 20240401), lte(date, 20240407))"
    }
    
    ```
    
3. This structured query is used to search your vector database, filtering for documents within that specific date range and then ranking them based on relevance to "projects excited about".

The magic here is that the SelfQuery Retriever can handle a wide range of natural language date queries:

- "What did I work on last summer?"
- "Show me my thoughts on AI from Q1 2024"
- "Any breakthroughs in my research during the holiday season?"

It understands these temporal expressions and converts them into precise date ranges for searching your notes.

The result? A chatbot that feels like it has an intuitive understanding of time, capable of retrieving memories and information from specific periods in your life with remarkable accuracy. It's like having a personal historian who knows exactly when and where to look in your vast archive of experiences.

This capability is particularly powerful for:

- Tracking progress on long-term projects
- Recalling ideas or insights from specific time periods
- Understanding how your thoughts or focus areas have evolved over time

With the SelfQuery Retriever, your Obsidian chatbot doesn't just search your notes – it understands the temporal context of your knowledge, making it an invaluable tool for reflection, planning, and personal growth.

But how does the chatbot know when each note was created? Let's explore how we've added this crucial information to our system.

### 3. Adding Date Metadata: Timestamping Your Thoughts

To support date-based queries and make the SelfQuery Retriever truly effective, we needed a way to associate each note with its creation date. This is where date metadata comes into play. I’ve implemented a  system to extract the date from each note's filename and add it as metadata during the indexing process:

```python
def extract_date_from_filename(filename: str) -> Optional[int]:
    match = re.match(r"(\\d{4}-\\d{2}-\\d{2})", filename)
    if match:
        date_str = match.group(1)
        try:
            date_obj = datetime.strptime(date_str, DATE_FORMAT)
            return int(date_obj.strftime("%Y%m%d"))
        except ValueError:
            return None
    return None

# In the indexing process
document.metadata["date"] = extract_date_from_filename(file)

```

This metadata allows our SelfQuery Retriever to efficiently filter documents based on date ranges or specific dates mentioned in user queries. It's like giving each of your notes a timestamp, allowing the chatbot to organize and retrieve them chronologically when needed.

With our chatbot now able to understand both the content and the temporal context of your notes, we've added one more crucial element to make it even more helpful: the ability to remember and use information from your conversation.

### 4. Enhancing MultiQuery Retriever with Chat History: Context-Aware Question Generation

In our previous iteration, we already used chat history to provide context for our LLM's responses. However, we've now taken this a step further by incorporating chat history into our MultiQuery Retriever. This enhancement significantly improves the chatbot's ability to understand and respond to context-dependent queries, especially in ongoing conversations.

Let's see how this works in practice:

Imagine you're having a conversation with your chatbot about your work projects:

You: "What projects did I work on March 1?"
Chatbot: [Provides a response about your March 1 projects]

You: "How about March 2?"

Without context, the MultiQuery Retriever might generate variations like:

1. "What happened on March 2?"
2. "Events on March 2"
3. "March 2 activities"

These queries, while related to the date, miss the crucial context about projects.

However, with our chat history-aware MultiQuery Retriever, it might generate variations like:

1. "What projects did I work on March 2?"
2. "Project activities on March 2"
3. "March 2 project updates"

These variations are much more likely to retrieve relevant information about your projects on March 2, maintaining the context of your conversation.

This improvement is crucial for maintaining coherent, context-aware conversations. Without it, the MultiQuery Retriever could sometimes generate less useful variations, particularly in multi-turn interactions where the context from previous messages is essential.

By making the MultiQuery Retriever aware of chat history, we've significantly enhanced its ability to generate relevant query variations. This leads to more accurate document retrieval and, ultimately, more contextually appropriate responses from the chatbot.

This enhancement truly brings together the power of our previous improvements. The MultiQuery Retriever now not only casts a wider net with multiple phrasings but does so with an understanding of the conversation's context. Combined with our SelfQuery Retriever's ability to handle temporal queries and our robust date metadata, we now have a chatbot that can navigate your personal knowledge base with remarkable context awareness and temporal understanding.

## Custom Implementations: Tailoring the Tools to Our Needs

To achieve these enhancements, we created several custom classes, each designed to extend the capabilities of Langchain's base components. Let's take a closer look at two key custom implementations:

1. CustomMultiQueryRetriever: This class extends the base MultiQueryRetriever to incorporate chat history in query generation.
2. CustomSelfQueryRetriever: We customized the SelfQuery Retriever to work seamlessly with our Pinecone vector store and handle date-based queries effectively.

Here's a snippet from our CustomMultiQueryRetriever to give you a taste of how we've tailored these components:

```python
class CustomMultiQueryRetriever(MultiQueryRetriever):
    def _get_relevant_documents(
        self,
        query: str,
        history: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> List[Document]:
        queries = self.generate_queries(query, history, run_manager)
        if self.include_original:
            queries.append(query)
        documents = self.retrieve_documents(queries, run_manager)
        return self.unique_union(documents)

    def generate_queries(
        self, question: str, history: str, run_manager: CallbackManagerForRetrieverRun
    ) -> List[str]:
        response = self.llm_chain.invoke(
            {"question": question, "history": history},
            config={"callbacks": run_manager.get_child()},
        )
        if isinstance(self.llm_chain, LLMChain):
            lines = response["text"]
        else:
            lines = response
        return lines

```

These custom implementations allow us to tailor the retrieval process to our specific needs, improving the overall performance and relevance of the chatbot's responses.

While these enhancements have significantly improved our chatbot, the journey wasn't without its challenges. Let's reflect on some of the hurdles we faced and the lessons we learned along the way.

## Challenges and Learnings: Navigating the Complexities of Langchain

While Langchain provides a powerful framework for building RAG systems, we found that its complexity can sometimes be challenging. Digging into different parts of the codebase to understand and modify behavior required significant effort. However, this process also provided valuable insights into the inner workings of RAG systems and allowed us to create a more tailored solution for our Obsidian chatbot.

Some key learnings from this process include:

- The importance of thoroughly understanding each component before attempting to customize it
- The value of incremental improvements and testing each change individually
- The need for patience when working with complex, interconnected systems

These challenges, while sometimes frustrating, ultimately led to a deeper understanding of RAG systems and a more robust final product.

Now that we've enhanced our chatbot with these powerful features, let's explore some of the exciting ways it can be used.

## Use Cases and Examples: Putting Our Enhanced Chatbot to Work

With these improvements, our Obsidian chatbot is now capable of handling a wider range of queries with improved accuracy. Here are some example use cases that showcase its new capabilities:

1. Date-specific queries: "What projects was I working on in the first week of March 2024?"
2. Context-aware follow-ups: "Tell me more about the meeting I had last Tuesday."
3. Complex information retrieval: "Summarize my progress on Project X over the last month."

These examples demonstrate the chatbot's ability to understand temporal context, maintain conversation history, and provide more relevant responses. It's not just a search tool anymore – it's becoming a true digital assistant that can help you navigate and make sense of your personal knowledge base.

As exciting as these improvements are, we're not stopping here. Let's take a quick look at what's on the horizon for our Obsidian chatbot.

## Future Plans: The Road Ahead

While we've made significant strides in improving our chatbot, there's always room for further enhancements. One exciting avenue we're exploring is the integration of open-source LLMs to make the system more privacy-focused and self-contained. This could potentially allow users to run the entire system locally, ensuring complete privacy of their personal notes and queries.

## Conclusion: A Smarter, More Intuitive Chatbot for Your Personal Knowledge Base

By implementing advanced RAG techniques such as MultiQuery Retriever, SelfQuery Retriever, and incorporating chat history, we've significantly enhanced our Obsidian chatbot's capabilities. These improvements allow for more accurate and contextually relevant responses, especially for date-based queries and complex information retrieval tasks.

Building this enhanced chatbot has been a journey of continuous learning and iteration. We've tackled challenges, discovered new possibilities, and created a tool that we hope will make navigating personal knowledge bases easier and more intuitive.

We hope that sharing our experience will inspire and help others in the community who are working on similar projects. Whether you're looking to build your own chatbot or simply interested in the possibilities of AI-assisted knowledge management, we hope this post has provided valuable insights.

You can find the final code in this [GitHub repo](https://github.com/prabha-git/obsidian_kb)

If you have any feedback or simply want to connect, please hit me up on [LinkedIn](https://www.linkedin.com/in/prabha-arivalagan/) or [@prabha-tweet](https://twitter.com/prabhatweet)