#!/usr/bin/env python3

import requests
from logzero import logger
import json
from pathlib import Path



# Account configuration file path
ACCOUNT_CONFIG_PATH = str(Path().resolve()) + "/account_configuration/"

""" Class to handle calls to Instagram Graph API """


class GraphHandler:

    def __init__(self, args):
        self.args = args
        self.info = dict()
        self.base_url = args.graph_api_base_path + args.graph_api_version

    def get_account_info(self):
        """ Fetches account information for the account. """

        logger.info("Fetching account information from Graph API.")
        # Setting extra fields for info dict
        self.info['account'] = []
        # Creating payload
        payload = {'access_token': self.args.graph_api_access_token}
        # Setting url to fetch information about current Graph API user
        url = self.base_url + 'me/accounts'
        # Sending request
        resp = requests.get(url, params=payload)

        # Checking that status is OK
        if resp.status_code == 200:
            resp_data = resp.json()
            # Making sure response data contains data key
            if "data" in resp_data:
                # Processing every account
                for account in resp_data['data']:
                    # Combining name and page ID into dict
                    account_dict = {'page_id': account['id']}
                    # Pushing dict into account info
                    self.info['account'].append(account_dict)

    def get_business_user_id(self):
        """ Gets Instagram Business User identifier"""

        logger.info("Querying business account user identifier.")
        if self.info['account']:
            # Setting payload to fetch Instagram business account id
            payload = {'access_token': self.args.graph_api_access_token,
                       'fields': 'instagram_business_account'}

            account = self.info['account'][0]
            url = self.base_url + account['page_id']
            logger.info('Sending GET request to url: ' + url)
            # Sending request
            resp = requests.get(url, params=payload)

            if resp.status_code == 200:
                resp_data = resp.json()
                if 'instagram_business_account' in resp_data:
                    logger.info(
                        "Received user id " + resp_data['instagram_business_account']['id'])
                    # Setting the received IG user id to the account's dict
                    account['user_id'] = resp_data['instagram_business_account']['id']


    def create_configuration_files(self):
        """ Creates/updates configuration files for the Instagram account. """

        logger.info("Creating configuration file.")
        # Calling function that creates dictionary of user info
        self.set_up_info()

        if self.info and 'account' in self.info:
            account = self.info['account'][0]
            # Constructing file name
            file_name = ACCOUNT_CONFIG_PATH + account['user_id'] + ".json"
            # If configuration file for the specific account already exists,
            # open in r+ mode to avoid overwriting.
            if Path(file_name).is_file():
                conf_file = open(file_name, 'r+')
                conf_data = json.load(conf_file)
                # Updating name, since only it can be changed.
                conf_data['name'] = account['name']
                # Moving pointer back to the beginning of the file.
                conf_file.seek(0)
                # Writing updated values
                json.dump(conf_data, conf_file, indent=4)
            else:
                conf_file = open(file_name, 'w')
                json.dump(account, conf_file, indent=4)
            # Closing file
            conf_file.close()


    def publish_video(self, creation_id, user_id):
        """ Publishes given video to Instagram account. """

        logger.info("Publishing video.")
        payload = {'access_token': self.args.graph_api_access_token,
                   'creation_id': creation_id}
        url = self.base_url + user_id + "/media_publish"
        logger.info("Sending POST request to url: " + url)
        resp = requests.post(url, params=payload)

        if resp.status_code == 200:
            logger.info("Post successfully published!")
        else:
            logger.warning(
                "Response from video publishing query is not OK.")
            logger.info(resp.json())

    def create_media_container(self, post_data):
        """ Creates Instagram media container """

        logger.info("Creating Instagram media container.")
        # Setting image url and caption to payload
        payload = {'access_token': self.args.graph_api_access_token,
                   'video_url': post_data['video_url'],
                   'caption': post_data['caption']}
        url = self.base_url + post_data['user_id'] + "/media"
        logger.info("Sending POST request to url: " + url + "/media")
        resp = requests.post(url, params=payload)

        if resp.status_code == 200:
            logger.info("Media container successfully created.")
            # Getting creation id as the response
            creation_id = resp.json()['id']
            # Calling publishing function
            self.publish_video(creation_id, post_data['user_id'])
        else:
            logger.warning("Creation of media container failed.")
            logger.info(resp.json())

    def set_up_info(self):
        """ Fetches information needed for API calls and post publishing """

        self.get_account_info()
        self.get_business_user_id()


    def construct_caption(self, acc_data):
        """ Constructs post caption from multiple strings. """

        logger.info("Constructing post caption.")
        caption = "Plant test."
        if 'hashtags' in acc_data and acc_data['hashtags']:
            # Adding hashtags as space delimited string
            caption += '\n' * 2 + " ".join(acc_data['hashtags'])
        else:
            logger.warning('Post hashtags not found.')

        return caption

    def start_posting_process(self):
        """ Starts the process of posting the watering video."""

        # Read configuration file into memory
        for p in Path(ACCOUNT_CONFIG_PATH).glob('*.json'):
            # Loading account configuration data into dictionary
            acc_data = json.loads(p.read_text())
            # Setting flag to ensure that required information exists.
            post_valid = True
            # Creating temporary dict to store individual post related information
            post_data = dict()
            post_data['user_id'] = acc_data['user_id']
            logger.info(
                "Starting posting process.")

            """
            # Getting video.
            try:
                
            except KeyError as exc:
                post_valid = False
            """

            # Constructing caption for the post.
            post_data['caption'] = self.construct_caption(acc_data)

            # If post is valid, creating media container.
            if post_valid:
                self.create_media_container(post_data)
            else:
                logger.warning("Skipping publishing video.")