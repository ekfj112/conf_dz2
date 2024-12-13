from graphviz import Digraph


def build_graph_image(graph_data, output_path):
    # Создаем объект графа
    dot = Digraph(format='png')

    # Добавляем ребра в граф
    for parent, children in graph_data.items():
        for child in children:
            dot.edge(child, parent)

    # Сохраняем граф в виде изображения
    dot.render(output_path, cleanup=True)


# Пример графа
graph_data = {
    'fb75313bad6458c96b83250e48ca24cf715343bc': ['e8c688075aba7d989ac82e32fd3e3266835b7275',
                                                 '2795d1db1675e08ac6e691faee28356d26789817'],
    'e8c688075aba7d989ac82e32fd3e3266835b7275': ['93f2241284fa9d67581c6ba18ca0816d1e2cbb56'],
    '2795d1db1675e08ac6e691faee28356d26789817': ['93f2241284fa9d67581c6ba18ca0816d1e2cbb56'],
    '93f2241284fa9d67581c6ba18ca0816d1e2cbb56': ['aa07f7ab85b85a91eb0eeae56c04c00292bdf987'],
    'aa07f7ab85b85a91eb0eeae56c04c00292bdf987': []
}

# Путь к файлу, куда сохранить граф
output_file = 'commit_graph'
build_graph_image(graph_data, output_file)
print(f"Граф сохранен в {output_file}.png")
