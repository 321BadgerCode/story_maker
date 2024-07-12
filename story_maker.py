import sys
import os
import re
import requests
import base64

def convert_to_filename(txt:str) -> str:
	invalid_chars:list = ["\\", "\n", "/", ":", "*", "?", "\"", "<", ">", "|"]
	for char in invalid_chars:
		txt = txt.replace(char, "")
	return txt.replace(" ", "_").lower()

class txt_gen:
	url:str = ""
	headers:dict = {}
	history:list = []
	data:dict = {}

	def __init__(self:object) -> None:
		self.url = "http://127.0.0.1:5000/v1/chat/completions"
		self.headers = {
			"Content-Type": "application/json"
		}
		self.data = {
			"mode": "chat",
			"character": "Assistant",
			"max_tokens": 1000,
			"messages": ""
		}
	def gen(self:object, prompt:str, max_tokens:int = 1000) -> str:
		self.history.append({"role": "user", "content": prompt})
		self.data["messages"] = self.history
		response:dict = requests.post(self.url, headers=self.headers, json=self.data, verify=False)
		assistant_message:str = response.json()['choices'][0]['message']['content']
		self.history.append({"role": "assistant", "content": assistant_message})
		return assistant_message

class img_gen:
	url:str = ""
	headers:dict = {}
	data:dict = {}
	pos_prompt:str = ""
	neg_prompt:str = ""

	def __init__(self:object, pos_prompt:str = "", neg_prompt:str = "bad_prompt_version2-neg FastNegativeV2 realisticvision-negative-embedding ugly, deformed, bad anotomy, bad lighting,") -> None:
		self.url = "http://127.0.0.1:7861/sdapi/v1/txt2img"
		self.headers = {
			"Content-Type": "application/json"
		}
		self.data = {
			"prompt": f"{pos_prompt}",
			"negative_prompt": f"{neg_prompt}",
			"width": 512,
			"height": 768,
			"restore_faces": True,
			"steps": 15
		}
	def gen(self:object, prompt:str, filename:str) -> None:
		self.data["prompt"] += prompt
		response:dict = requests.post(self.url, headers=self.headers, json=self.data, verify=False)
		txt:str = response.json()['images'][0]
		with open(f"{filename}", "wb") as file:
			file.write(base64.b64decode(txt))

prompt:str = ""
loras:str = ""
max_tokens:int = 1000
pos_prompt_prefix:str = ""
for i in range(1, len(sys.argv)):
	if sys.argv[i] == "-h" or sys.argv[i] == "--help":
		print(f"Usage: python {sys.argv[0]} -p <prompt> -l <lora models> -t <max text tokens> -pp <positive prompt prefix>")
		sys.exit(0)
	elif sys.argv[i] == "-p" or sys.argv[i] == "--prompt":
		prompt = sys.argv[i + 1]
		break
	elif sys.argv[i] == "-l":
		loras = sys.argv[i + 1]
		loras = "<lora:" + loras.replace(",", ":1> <lora:") + ":1>"
		break
	elif sys.argv[i] == "-t":
		max_tokens = int(sys.argv[i + 1])
		break
	elif sys.argv[i] == "-pp":
		pos_prompt_prefix = sys.argv[i + 1]
		break
if prompt == "":
	print("Input the summary of the story.")
	prompt = input("> ")

user_message = f"""
Generate a story based on the following summary:

{prompt}

For images, prefix the image with a `(image)` and then encapsulate the caption of the image in square brackets. For example:

(image)[brave knight fighting a dragon, knight armor, dragon fire, long sword]
"""
user_message = user_message.replace("\n", "\\n")

txt_gen_obj:object = txt_gen()
story:str = txt_gen_obj.gen(user_message, max_tokens)

filename:str = convert_to_filename(prompt)
if not os.path.exists(f"./{filename}/"):
	os.makedirs(f"./{filename}/")
with open(f"./{filename}/story.md", "w") as f:
	f.write(story)

pattern = r"\(image\)\[(.*?)\]"
matches = re.findall(pattern, story)
img_gen_obj:object = img_gen(loras + f"masterpiece, absurdres, 8k, hd, best quality, {pos_prompt_prefix}")
for match in matches:
	img_filename:str = f"./{filename}/{convert_to_filename(match)}.png"
	img_gen_obj.gen(match, img_filename)
	story = story.replace(f"(image)[{match}]", f"![{match}]({img_filename})")
	with open(f"./{filename}/story.md", "w") as f:
		f.write(story)