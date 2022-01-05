import configargparse


def get_configuration():
    p = configargparse.ArgParser(
        default_config_files=['/etc/app/conf.d/*.conf', '~/.my_settings'])
    p.add('-c', '--my-config', required=True,
          is_config_file=True, help='config file path')
    p.add('-a', '--configure_account', required=False, action='store_true',
          help='Argument used for creating account configuration file.')
    p.add('--graph_api_access_token', required=True, help='Access Token')
    p.add('--graph_api_version', required=True,
          help='Version of the Instagram Graph API')
    p.add('--graph_api_base_path', required=True,
          help='Base path for Instagram Graph API')
    p.add('--file_io_api_key', required=True,
          help='API Key for File.io API')
    p.add('--file_io_base_path', required=True,
          help='Base path for File.io API')
    p.add('--image_name_prefix', required=True,
          help='prefix for image file')
    p.add('--video_name_prefix', required=True,
          help='prefix for video file')
    p.add('--database_name', required=True,
          help='name of sqlite database')

    options = p.parse_args()

    return options
