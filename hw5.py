import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from typing import Union
import os.path as path


class QuestionnaireAnalysis:
    """
    Reads and analyzes data generated by the questionnaire experiment.
    Should be able to accept strings and pathlib.Path objects.
    """
    
    def __init__(self, data_fname: Union[pathlib.Path, str]):
        if not path.exists(data_fname):
            raise ValueError
        if type(data_fname) == str:
            self.data_fname = pathlib.Path(data_fname)
        else:
            self.data_fname = data_fname
        self.data = None

    def read_data(self):
        """
        Reads the json data located in self.data_fname into memory, to
        the attribute self.data.
        """
        self.data = pd.read_json(self.data_fname)

    def show_age_distrib(self):
        """
        Calculates and plots the age distribution of the participants.
        Returns a tuple containing two numpy arrays:
        The first item being the number of people in a given bin.
        The second item being the bin edges.
        """
        ages = self.data['age'][~self.data['age'].isna()]
        [hist, bins] = np.histogram(ages, range=(0, 100))
        fig = plt.figure(figsize=(10, 10))
        plt.hist(ages, bins=bins)
        plt.show()
        return hist, bins

    def remove_rows_without_mail(self) -> pd.DataFrame:
        """
        Checks self.data for rows with invalid emails, and removes them.
        Returns the corrected DataFrame, i.e. the same table but with
        the erroneous rows removed and the (ordinal) index after a reset.
        """
        email_reg = r'.+@.+\..+'
        self.data = self.data[
            self.data['email'].str.contains(email_reg)
        ]
        self.data = self.data.reset_index()
        return self.data

    def fill_na_with_mean(self) -> Union[pd.DataFrame, np.ndarray]:
        """
        Finds, in the original DataFrame, the subjects that didn't answer
        all questions, and replaces that missing value with the mean of the
        other grades for that student. Returns the corrected DataFrame,
        as well as the row indices of the students that their new grades
        were generated.
        """
        inds = np.array([])
        questions = ['q1', 'q2', 'q3', 'q4', 'q5']
        for q in questions:
            nans = self.data[q].isna()
            self.data.loc[nans, q] = np.nanmean(self.data[questions][nans], 1)
            inds = np.union1d(inds, nans[nans].index)
        return [self.data, inds]

    def correlate_gender_age(self) -> pd.DataFrame:
        """
        Looks for a correlation between the gender of the subject, their age
        and the score for all five questions.
        Returns a DataFrame with a MultiIndex containing the gender and whether
        the subject is above 40 years of age, and the average score in each of
        the five questions.
        """
        g = self.data[['gender', 'q1', 'q1', 'q1', 'q1']].groupby(['gender', self.data.age > 40])
        return g.mean()


if __name__ == '__main__':
    #qa = QuestionnaireAnalysis('data.json')
    #qa.remove_rows_without_mail()
    import test_qs
    test_qs.test_email_validation()
