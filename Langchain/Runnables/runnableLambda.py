from langchain.schema.runnable import RunnableLambda

def words_count(text):
    return len(text.split())

runnable_word_count = RunnableLambda(words_count)

res = runnable_word_count.invoke('Hello world, this is a test.')

# this way we cam make any function into a runnable and use it in our chains. We can also use it to create custom runnables that can be used in our chains.