<p align="center">
	<img src="./asset/logo.png" alt="Story Maker Logo" width="200" height="200">
</p>

<h1 align="center">Story Maker</h1>

<p align="center">
	<strong>Creates stories with images by using AI API's!</strong>
</p>

## 🚀 Overview

Welcome to the **Story Maker**! This project allows you to create stories with images by just typing a summary of the story.

## 🎨 Features

- **Image Generation:** Generates images based on the story summary.
- **Custom Loras:** Accepts local lora models to customize the image generation to be specific for the exact story.

## 🛠️ Installation

To get started with the Story Maker, there is only **one** step!

1. **Clone the Repository**
```sh
git clone https://github.com/321BadgerCode/story_maker.git
cd ./story_maker/
```

<details>

<summary>Dependencies</summary>

**Dependencies**:
- [Oobabooga](https://github.com/oobabooga/text-generation-webui "Common text generation webUI") needs to be running locally using it's API feature on port 5000 (default): http://127.0.0.1:5000/
	- **Model:** *Any*
- [Automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui "Common stable diffusion webUI") needs to be running locally using it's API feature on port 7861 (not default since port 7860 is taken by Oobabooga): http://127.0.0.1:7861/
	- **Model:** *Any*
	- **Embeddings:** bad_prompt_version2-neg FastNegativeV2 realisticvision-negative-embedding
	- **Face Restoration Model:** *Any*

</details>

## 📝 Usage

To use the Story Maker, there is only **one** step!

1. **Run the Story Maker**
```sh
python ./main.py
```

<details>

<summary>💻 Command Line Arguments</summary>

**Command Line Arguments**:

> [!NOTE]
> The lora models should be separated by comma, so like `python ./main.py -l <lora:model:1>,<lora:other_model:1>`.
|	Argument		|	Description					|
|	:---:			|	:---:						|
|	`-h & --help`		|	Show help message				|
|	`-p & --prompt`		|	Prompt for the story				|
|	`-l`			|	Lora models for the story			|
|	`-t`			|	Max amount of tokens for the story generator	|
|	`-pp`			|	Positive prompt prefix like `beatiful, cool,`	|

</details>

## 📝 License

[LICENSE](./LICENSE)
