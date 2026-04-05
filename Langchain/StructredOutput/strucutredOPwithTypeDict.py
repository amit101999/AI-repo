
from typing import TypedDict  ,Annotated

class Person(TypedDict):
    name: str
    age: int
    city: str

new_person = Person(name="Alice", age=30, city="New York")
# also it jsut tell we can put other type of values in the dict but it will not give us any error but it will give us a warning
print(new_person)



from lancghai_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


model = ChatOpenAI(model="gpt-3.5-turbo" , temperature=0.9)

class Review(TypedDict):
    title: str
    summary: @Annotated[str , "A brief summary of the review"]
    # now since if the llm dont undersand the type hint we can add a comment to the type hint to tell the model what type of value we want for that key in annotated
    rating: int
    comment: str
    key_themes: @Annotated[list[str] , "A list of key themes discussed in the review"]
    pros :@Annotated[Optional[list[str]], "A list of pros of the review"]


    strutcured_model = model.with_structured_output(Review)

result = strutcured_model.invoke("Write a review for the movie Inception")
# now this will give us a dict with the keys title , rating and comment and the values will be the review for the movie Inception
# byt giving this the model will genrate a new system prompt that will tell the model to generate a review for the movie Inception in the form of a dict with the keys title , rating and comment

# now since this just tell the output but it does not mean it will  the same format now to validate the data we use the pydantic model to validate the data and if the data is not in the correct format it will give us an error