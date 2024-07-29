import json

if __name__ == '__main__':
    dir_name = 'v2'
    full_jd = []
    for i in range(101):
        with open(f"{dir_name}/jobs-{i}.json", "r", encoding='utf8') as f:
            full_jd += json.load(f)

    with open(f'full_jd.json', 'w', encoding='utf8') as f:
        json.dump(full_jd, f, indent=2, ensure_ascii=False)
