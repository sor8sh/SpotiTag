from SpotiTag import SpotiTag


# your OAuth Token
token = ""
if token == "":
    token = input("Insert your OAuth Token: ")

# your tag (search key)
tag = ""
if tag == "":
    tag = input("Insert your search key (tag): ")

spotiTag = SpotiTag(
    token=token,
    tag=tag,
    output_dir='./output',
    write=True
)
spotiTag.run()
