from pathlib import Path
import pickle

class DataHandler:
    def __init__(self, data_folder):
        self.rawDataFolder = Path(data_folder)
        print(self.rawDataFolder)
        self.load_raw_data()

    def unpickle_file(self, filename):
        path = Path(self.rawDataFolder, filename)
        with path.open('rb') as fp:
            content = pickle.load(fp)
        return content

    def load_raw_data(self):
        self.raw_pdCommits = self.unpickle_file("Commits.p")
        self.raw_pdReleases = self.unpickle_file("GitReleases.p")
        self.raw_pdEdits = self.unpickle_file("Edits.p")
        self.raw_pdIssues = self.unpickle_file("Issues.p")
        self.raw_pdRepositories = self.unpickle_file("Repositories.p")
        self.raw_pdPullRequests = self.unpickle_file("PullRequests.p")
        self.raw_pdUsers = self.unpickle_file("Users.p")