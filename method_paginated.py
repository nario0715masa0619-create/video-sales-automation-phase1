    def search_channels_paginated(self, keyword: str, max_results: int = 150) -> List[str]:
        '''キーワードからチャンネルを検索（ページネーション対応、最大150チャンネル）'''
        # キャッシュから取得
        cached = self.cache.get_search_results(keyword)
        if cached:
            logger.info(f'検索キャッシュヒット: {keyword} ({len(cached)} チャンネル)')
            return cached[:max_results]

        logger.info(f'YouTube 検索開始: {keyword} (最大 {max_results} チャンネル)')

        all_channel_ids = []
        page_token = None
        pages = (max_results + 49) // 50

        for page in range(pages):
            params = {
                'part': 'snippet',
                'q': keyword,
                'type': 'channel',
                'maxResults': min(50, max_results - len(all_channel_ids)),
                'relevanceLanguage': 'ja',
                'regionCode': 'JP',
                'order': 'relevance',
            }
            
            if page_token:
                params['pageToken'] = page_token

            endpoint = f'{self.base_url}/search'
            data, quota = self._request_with_etag('GET', endpoint, params, f'search:{keyword}:page{page}')

            if not data:
                break

            for item in data.get('items', []):
                if item.get('id', {}).get('kind') == 'youtube#channel':
                    channel_id = item['id']['channelId']
                    all_channel_ids.append(channel_id)
                    if len(all_channel_ids) >= max_results:
                        break

            page_token = data.get('nextPageToken')
            if not page_token or len(all_channel_ids) >= max_results:
                break

            time.sleep(1.0)

        self.cache.set_search_results(keyword, all_channel_ids)
        logger.info(f'検索完了: {keyword} → {len(all_channel_ids)} チャンネル')
        return all_channel_ids
