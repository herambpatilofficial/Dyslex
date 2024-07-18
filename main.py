import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
import json
model = genai.GenerativeModel(model_name = "gemini-pro")

prompt_parts = [
    """
"Create a captivating and interactive short story for children that helps improve their vocabulary, particularly focusing on dyslexic learners. The story should include a variety of words that are often confusing due to their similarity in spelling or sound, such as CAT, MAT, BAT, HAT, PAT, and SAT. Ensure the story is engaging and places these words in different contexts to aid understanding. Additionally, provide options for the child to tap on words to get their definitions or see them used in other sentences. The narrative should be simple, fun, and educational, encouraging children to learn and understand the words through context. Incorporate a mix of familiar and new words to support the learning process."

**Example Words:**
CAT, MAT, BAT, HAT, PAT, SAT, DOG, LOG, FROG, HOP, TOP, MOP

**Desired Features:**

- **Contextual Learning:** Use each word in various sentences to help the child understand their meaning.
- **Interactive Elements:** Allow the child to tap on words to get definitions or additional examples.
- **Engaging Storyline:** Keep the story fun and interesting to maintain the child's attention.
- **Educational Focus:** Encourage vocabulary development and comprehension through repetition and contextual usage.
- **Simplicity:** Use simple English, use language which toddlers can understand, keep stories short, loving, interesting.

Following is example output, give story and json seperately with markdown in triple backticks and give interactive elements and their meaning in simple English in JSON format

**Example Output:**

---
```
**Title: "Timmy's Amazing Adventure"**

One bright morning, Timmy woke up with a big smile. Today, he planned to explore the forest near his house. As he walked down the path, he saw a fluffy **CAT** lounging on a colorful **MAT**. "Good morning, Mr. Whiskers!" Timmy said, giving the cat a gentle **PAT** on its head.

Timmy continued his adventure and found a **BAT** hanging upside down from a tree branch. "Look at you, little **BAT**!" he exclaimed. Nearby, a cute **DOG** was playing with a fallen **LOG**. Timmy laughed as the **DOG** chased a hopping **FROG** around the **LOG**.

As Timmy ventured deeper into the forest, he put on his favorite red **HAT** to shield himself from the sun. He saw a tall tree with a big, comfy **MAT** underneath it. Feeling tired, Timmy decided to sit down on the **MAT** and rest for a while.

Suddenly, Timmy heard a rustling sound. He turned around and saw a little bird perched on a **LOG**. The bird chirped happily and flew up to the **TOP** of the tree. Timmy stood up and decided to follow the bird. He grabbed a **MOP** lying nearby and used it to clear the path.

Timmy had a wonderful time in the forest, meeting new animal friends and discovering new things. As the sun began to set, he made his way back home, feeling happy and excited about his next adventure.
```
---

**Interactive Elements:**
```json
{
  "CAT": "A small domesticated carnivorous mammal.",
  "MAT": "A thick piece of material used for wiping or cleaning.",
  "BAT": "A club used in the sport of baseball or a flying mammal.",
  "HAT": "A covering for the head.",
  "PAT": "To tap lightly with the palm of the hand.",
  "SAT": "To be in a sitting position.",
  "DOG": "A domesticated carnivorous mammal.",
  "LOG": "A large piece of wood.",
  "FROG": "A small tailless amphibian.",
  "HOP": "To jump on one foot.",
  "TOP": "The highest point or part of something.",
  "MOP": "A tool for cleaning floors."
}
```
---


    """,
]

#store triple backticks in two variables
def story_extracted(response):
  print(response)
  story = response.split("```")[1]
  
  return story

def get_proper_json(interactive_elements):
  
  response = model.generate_content(f"Return in the JSON in this text in json format which I can directly parse don't add anything else, no markdown : {interactive_elements}")
  return response.text


def generate_story():
  # Replace with actual Gemini API call
  story = model.generate_content(f"{prompt_parts}").text
  interactive_elements = get_proper_json(story)
  story = story_extracted(story)


  return story, interactive_elements

# Title and Introduction
st.title("Dyslexia Learning Assistant")
st.write("This app helps dyslexic kids learn new words in a fun way!")

# Input Text
story,interactive_elements = generate_story()
# text = st.text_area(story)

interactive_elements_json = json.dumps(interactive_elements)

# Streamlit app
st.title("Interactive Story for Dyslexic Children")
st.markdown("### A Story to Improve Vocabulary")

# Generate and display the story
story = generate_story()
st.markdown(story, unsafe_allow_html=True)

# Display the JSON with word meanings
st.markdown("""
    <script>
    const meanings = JSON.parse("{}");
    document.querySelectorAll('.clickable').forEach(elem => {
        elem.addEventListener('click', event => {
            const word = event.target.id;
            alert(meanings[word]);
        });
    });
    </script>
""".format(interactive_elements), unsafe_allow_html=True)



# # Highlight Functionality (simplified for now)
# highlighted_word = None
# if st.button("Highlight a Difficult Word"):
#   highlighted_word = st.text_input("Enter the highlighted word:")

# # Generate Story with Gemini Integration (placeholder)
# if highlighted_word:
#   generated_story = generate_story(highlighted_word)
#   st.write("**New Story:**")
#   st.write(generated_story)
# else:
#   st.write("Please highlight a word to generate a new story.")

# # Display Original Text
# st.write("**Original Text:**")
# st.write(text)

# # Note: This is a basic example. You'll need to implement the actual Gemini API call and handle responses.
