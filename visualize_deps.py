import os
import configparser
import subprocess
from pathlib import Path


def parse_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    paths = config["Paths"]
    return {
        "graphviz_tool": paths.get("graphviz_tool"),
        "repository_path": paths.get("repository_path"),
        "output_file": paths.get("output_file"),
        "target_file_hash": paths.get("target_file_hash"),
    }


def build_graphviz_graph(commits):
    from graphviz import Digraph
    graph = Digraph()

    for commit, parents in commits.items():
        if commit and parents:  # Проверяем, что и коммит, и его родители существуют
            for parent in parents:
                if parent:  # Проверяем, что родительский коммит не пустой
                    graph.edge(parent, commit)

    return graph


def save_graph(graph, output_path):
    # Получаем строку, представляющую граф в формате DOT
    dot_source = graph.source
    with open(output_path, "w") as f:
        f.write(dot_source)


def visualize(config_path):
    config = parse_config(config_path)
    commits = get_commit_dependencies(config["repository_path"], config["target_file_hash"])

    if not commits:
        print("No commits found for the target file hash.")
        return

    print(f"Commits found: {commits}")  # Отладочный вывод
    graph = build_graphviz_graph(commits)
    save_graph(graph, config["output_file"])
    print(graph)


def get_commit_dependencies(repo_path, target_hash):
    os.chdir(repo_path)
    git_log_cmd = 'git log --all --pretty=format:"%H %P" --name-only'

    result = subprocess.run(git_log_cmd, shell=True, text=True, capture_output=True)

    if result.returncode != 0:
        raise RuntimeError("Failed to fetch git log.")

    # Парсинг вывода
    commits = {}
    current_commit = None
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        if " " in line:  # Коммит и родители
            parts = line.split(" ")
            current_commit = parts[0]
            parents = parts[1:] if len(parts) > 1 else []
            commits[current_commit] = parents
        elif current_commit:  # Изменённые файлы
            # Проверяем, есть ли файл с нужным хешем
            if line.strip() == target_hash:
                print(f"Found target hash in commit {current_commit}")  # Отладка
                continue

    # Убираем пустые коммиты и родительские связи
    commits = {commit: parents for commit, parents in commits.items() if commit and parents}

    if not commits:
        print("No commits with the specified file hash found.")  # Отладка

    return commits


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Visualize Git commit dependencies.")
    parser.add_argument("config", help="Path to the configuration file.")
    args = parser.parse_args()

    visualize(args.config)
