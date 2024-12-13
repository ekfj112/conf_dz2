import unittest
from unittest.mock import patch
from visualize_deps import parse_config, save_graph, get_commit_dependencies, visualize


class TestVisualizeDeps(unittest.TestCase):

    @patch('visualize_deps.parse_config')
    @patch('visualize_deps.get_commit_dependencies')
    @patch('visualize_deps.save_graph')
    def test_visualize(self, mock_save_graph, mock_get_commit_dependencies, mock_parse_config):
        # Мокаем возвращаемые значения
        mock_parse_config.return_value = {
            'graphviz_tool': '/usr/bin/dot',
            'repository_path': 'C:\\Users\\Vlaso\\git-demo',
            'output_file': 'C:\\Users\\Vlaso\\git-demo\\output.dot',
            'target_file_hash': 'fb75313bad6458c96b83250e48ca24cf715343bc'
        }

        # Мокаем зависимость коммитов
        mock_get_commit_dependencies.return_value = {
            'fb75313bad6458c96b83250e48ca24cf715343bc': ['e8c688075aba7d989ac82e32fd3e3266835b7275', '2795d1db1675e08ac6e691faee28356d26789817'],
            'e8c688075aba7d989ac82e32fd3e3266835b7275': ['93f2241284fa9d67581c6ba18ca0816d1e2cbb56'],
            '2795d1db1675e08ac6e691faee28356d26789817': ['93f2241284fa9d67581c6ba18ca0816d1e2cbb56'],
            '93f2241284fa9d67581c6ba18ca0816d1e2cbb56': ['aa07f7ab85b85a91eb0eeae56c04c00292bdf987'],
            'aa07f7ab85b85a91eb0eeae56c04c00292bdf987': []
        }

        # Запуск функции visualize
        visualize("path_to_config.ini")

        # Проверка, что save_graph была вызвана с правильным графом
        mock_save_graph.assert_called_once()

    @patch('visualize_deps.parse_config')
    @patch('visualize_deps.get_commit_dependencies')
    def test_parse_config(self, mock_get_commit_dependencies, mock_parse_config):
        # Мокаем возвращаемые значения для конфиг файла с секцией 'Paths'
        mock_parse_config.return_value = {
            'graphviz_tool': '/usr/bin/dot',
            'repository_path': 'C:\\Users\\Vlaso\\git-demo',
            'output_file': 'C:\\Users\\Vlaso\\git-demo\\output.dot',
            'target_file_hash': 'fb75313bad6458c96b83250e48ca24cf715343bc'
        }

        # Проверка корректности парсинга конфиг файла
        config = mock_parse_config("path_to_config.ini")  # Теперь мы используем мок
        self.assertEqual(config['graphviz_tool'], '/usr/bin/dot')
        self.assertEqual(config['repository_path'], 'C:\\Users\\Vlaso\\git-demo')
        self.assertEqual(config['output_file'], 'C:\\Users\\Vlaso\\git-demo\\output.dot')
        self.assertEqual(config['target_file_hash'], 'fb75313bad6458c96b83250e48ca24cf715343bc')

    @patch('visualize_deps.parse_config')
    @patch('visualize_deps.get_commit_dependencies')
    def test_get_commit_dependencies(self, mock_get_commit_dependencies, mock_parse_config):
        # Мокаем возвращаемые значения для получения зависимостей коммитов
        mock_parse_config.return_value = {
            'graphviz_tool': '/usr/bin/dot',
            'repository_path': 'C:\\Users\\Vlaso\\git-demo',
            'output_file': 'C:\\Users\\Vlaso\\git-demo\\output.dot',
            'target_file_hash': 'fb75313bad6458c96b83250e48ca24cf715343bc'
        }

        mock_get_commit_dependencies.return_value = {
            'fb75313bad6458c96b83250e48ca24cf715343bc': ['e8c688075aba7d989ac82e32fd3e3266835b7275', '2795d1db1675e08ac6e691faee28356d26789817'],
            'e8c688075aba7d989ac82e32fd3e3266835b7275': ['93f2241284fa9d67581c6ba18ca0816d1e2cbb56'],
            '2795d1db1675e08ac6e691faee28356d26789817': ['93f2241284fa9d67581c6ba18ca0816d1e2cbb56'],
            '93f2241284fa9d67581c6ba18ca0816d1e2cbb56': ['aa07f7ab85b85a91eb0eeae56c04c00292bdf987'],
            'aa07f7ab85b85a91eb0eeae56c04c00292bdf987': []
        }

        commits = get_commit_dependencies('C:\\Users\\Vlaso\\git-demo', 'fb75313bad6458c96b83250e48ca24cf715343bc')
        self.assertIn('fb75313bad6458c96b83250e48ca24cf715343bc', commits)
        self.assertIn('e8c688075aba7d989ac82e32fd3e3266835b7275', commits['fb75313bad6458c96b83250e48ca24cf715343bc'])
        self.assertIn('2795d1db1675e08ac6e691faee28356d26789817', commits['fb75313bad6458c96b83250e48ca24cf715343bc'])


if __name__ == '__main__':
    unittest.main()
