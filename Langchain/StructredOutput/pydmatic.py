from pydantic import BaseModel
class Student(BaseModel):
    name: str ='Amit'  # we can also give default value to the keys in the pydantic model
    age: int
    city: str

new_student  = {"name": "Alice", "age": 30, "city": "New York"}
student = Student(**new_student)
# now we can not pass any other type of value in the  pydantic model because it will give us an error
print(type(student))

