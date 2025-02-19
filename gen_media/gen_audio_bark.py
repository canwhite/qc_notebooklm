from transformers import AutoProcessor, BarkModel
import scipy
import torch


voice_preset = "v2/en_speaker_6"
sampling_rate = 24000

device = "cuda:1" if torch.cuda.is_available() else "cpu"

processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark", torch_dtype=torch.float16).to(device)#.to_bettertransformer()

text_prompt = """
Exactly! [sigh] And the distillation part is where you take a LARGE-model,and compress-it down into a smaller, more efficient model that can run on devices with limited resources.
"""
inputs = processor(text_prompt, voice_preset=voice_preset).to(device)

with torch.no_grad():
    speech_output = model.generate(**inputs, temperature=0.9, semantic_temperature=0.8)

# Convert the output to a numpy array
speech_output_np = speech_output.cpu().numpy()

# Save the audio to a file
scipy.io.wavfile.write("bark_output_audio.wav", sampling_rate, speech_output_np)

#  


