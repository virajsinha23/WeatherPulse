
from pipeline import run_pipeline
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    run_pipeline(
        latitude=28.6139,
        longitude=77.2090,
        city="Delhi",
        country="India",
    )


if __name__ == "__main__":
    main()
