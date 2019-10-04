from GitHubCrawler.spiders.services import ConfigService
from GitHubCrawler.spiders.use_cases import SearchResultLinkExtractorUseCase, SearchUrlGeneratorUseCase


def build_search_url_generator() -> SearchUrlGeneratorUseCase:
    return SearchUrlGeneratorUseCase(ConfigService())


def build_git_search_result_extractor_use_case() -> SearchResultLinkExtractorUseCase:
    return SearchResultLinkExtractorUseCase()
