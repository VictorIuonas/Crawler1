from GitHubCrawler.spiders.use_cases import SearchResultLinkExtractorUseCase


def build_git_search_result_extractor_use_case() -> SearchResultLinkExtractorUseCase:
    return SearchResultLinkExtractorUseCase()
