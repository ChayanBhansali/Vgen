from vgen.pipeline.story import process_story

if __name__ == "__main__":
    stories = [""]
    story_ids = ["story1"]

    for sid, story in zip(story_ids, stories):
        print(f"Processing {sid}")
        result = process_story(story_id=sid, story=story)
        print(result)
