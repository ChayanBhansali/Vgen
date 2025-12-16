from vgen.pipeline.story import process_story

if __name__ == "__main__":
    stories = ["""AITA for wanting to keep my engagement ring from my late fiancé?
"""]
    story_ids = ["story2"]

    for sid, story in zip(story_ids, stories):
        print(f"Processing {sid}")
        result = process_story(story_id=sid, story=story , output_dir="./output", input_dir="./input")
        print(result)
