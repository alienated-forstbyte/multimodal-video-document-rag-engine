import whisper
import json
import copy

model = whisper.load_model("base")
result = model.transcribe("output.mp3")

print(result['text'])

chunk_template = {
    "chunk_id" : None,
    "start_time" : None,
    "end_time" : None,
    "formatted_time" : None,
    "text" : None,
    "frame_path" : None
}

chunks = []

with open("transcript.txt", "w", encoding="utf-8") as f:
    for i, segment in enumerate(result['segments']):

        start = segment['start']
        end = segment['end']
        text = segment['text'].strip()

        f.write(f"[{start:2f} --> {end:2f}] {text} \n")

        matching_second = int(start // 5 ) * 5
        matching_frame = f"frames/frame_{matching_second:04d}.jpg"

        chunk = copy.deepcopy(chunk_template)
        chunk['chunk_id'] = i
        chunk['start_time'] = start
        chunk['end_time'] = end
        chunk['formatted_time'] = f"{start:.2f} --> {end:.2f}"
        chunk['text'] = text
        chunk['frame_path'] = matching_frame
        
        chunks.append(chunk)

with open("metadata.json", "w", encoding="utf-8") as m :
    json.dump(chunks,m,indent=4,ensure_ascii=False)