import numpy as np
import json
import os
import random as random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.path import Path
import requests
from collections import Counter
import re
random.seed(17)


class DetroitDistrict:
    """
    A class representing a district in Detroit with attributes related to historical redlining.
    coordinates,holcGrade,holcColor,id,description should be load from the redLine data file
    if cache is not available

    Parameters
    ------------------------------
    coordinates : list of lists, 2D List, not list of list of list
        Coordinates defining the district boundaries from the json file
        Note that some districts are non-contiguous, which may
        effect the structure of this attribute

    holcGrade : str
        The HOLC grade of the district.

    id : str
        The identifier for the district, the HOLC ID.

    description : str, optional
        Qualitative description of the district.

    holcColor : str, optional
        A string represent the color of the holcGrade of the district

    randomLat : float, optional
        A random latitude within the district (default is None).

    randomLong : float, optional
        A random longitude within the district (default is None).

    medIncome : int, optional
        Median household income for the district, to be filled later (default is None).

    censusTract : str, optional
        Census tract code for the district (default is None).


    Attributes
    ------------------------------
    self.coordinates
    self.holcGrade
    holcColor : str
        The color representation of the HOLC grade.
        • Districts with holc grade A should be assigned the color 'darkgreen'
        • Districts with holc grade B should be assigned the color 'cornflowerblue'
        • Districts with holc grade C should be assigned the color 'gold'
        • Districts with holc grade D should be assigned the color 'maroon'
        If there is no input for holcColor, it should be generated based on the holcGrade and the rule above.

    self.id
    self.description
    self.randomLat
    self.randomLong
    self.medIncome
    self.censusTract


    """
    def __init__(self, coordinates, holcGrade, id, description, holcColor = None, randomLat=None, randomLong=None, medIncome=None, censusTract=None):
        self.coordinates = coordinates
        self.holcGrade = holcGrade
        self.id = id
        self.description = description
        self.holcColor = holcColor if holcColor else self._determine_color(holcGrade)
        self.randomLat = randomLat
        self.randomLong = randomLong
        self.medIncome = medIncome
        self.censusTract = censusTract

    def _determine_color(self, holcGrade):
        """
        Determines the color representation of the HOLC grade.

        Parameters
        ----------
        holcGrade : str
            The HOLC grade of the district.

        Returns
        -------
        str
            The color corresponding to the HOLC grade.
        """
        grade_to_color = {
            'A': 'darkgreen',
            'B': 'cornflowerblue',
            'C': 'gold',
            'D': 'maroon'
        }
        return grade_to_color.get(holcGrade, 'unknown')



class RedLines:
    """
    A class to manage and analyze redlining district data.

    Attributes
    ----------
    districts : list of DetroitDistrict
        A list to store instances of DetroitDistrict.

    """

    def __init__(self,cacheFile = None):
        """
        Initializes the RedLines class without any districts.
        assign districts attribute to an empty list
        """
        if cacheFile:
            if not self.loadCache(cacheFile):
                print(f"Failed to load cache from {cacheFile}. Initializing with an empty list.")
                self.districts = []
        else:
            self.districts = []


    def createDistricts(self, fileName):
        """
        Creates DetroitDistrict instances from redlining data in a specified file.
        Based on the understanding in step 1, load the file,parse the json object, 
        and create 238 districts instance.
        Finally, store districts instance in a list,
        and assign the list to be districts attribute of RedLines.

        Parameters
        ----------
        fileName : str
            The name of the file containing redlining data in JSON format.

        Hint
        ----------
        The data for description attribute could be from
        one of the dict key with only number.

        """
        with open(fileName, 'r') as f:
            data = json.load(f)

        # Extract the list of districts from the "features" key
        features = data.get('features', [])

        districts = []
        for feature in features:
            # Extract attributes from the JSON data
            geometry = feature.get('geometry', {})
            properties = feature.get('properties', {})

            coordinates = geometry.get('coordinates', [])
            holcGrade = properties.get('holc_grade', '')
            id = properties.get('holc_id', '')
            description = properties.get('area_description_data', {}).get('8', '')  # Use key '8' for description
            holcColor = None  # holcColor will be determined by the DetroitDistrict class

            # Create a DetroitDistrict instance
            district = DetroitDistrict(
                coordinates=coordinates,
                holcGrade=holcGrade,
                id=id,
                description=description,
                holcColor=holcColor
            )
            districts.append(district)

        # Ensure the districts are created in the order they appear in the data
        self.districts = districts

    def plotDistricts(self):
        """
        Plots the districts using matplotlib, displaying each district's location and color.
        Name it redlines_graph.png and save it to the current directory.
        """
        fig, ax = plt.subplots()
        for district in self.districts:  # Iterate over all districts
            for multipolygon in district.coordinates:  # Handle non-contiguous districts
                for polygon in multipolygon:
                    ax.add_patch(plt.Polygon(
                        polygon,
                        closed=True,
                        facecolor=district.holcColor, # Set the fill color to the district's HOLC color
                        edgecolor='black',  # Set the border color to black
                        alpha=0.5
                    ))
        ax.autoscale()
        plt.rcParams["figure.figsize"] = (15, 15)
        plt.show()
        plt.savefig('redlines_graph.png') # Save the plot as redlines_graph.png

    def generateRandPoint(self):
        """
        Generates a random point within the boundaries of each district.

        This method creates a mesh grid of points covering the geographical area of interest
        and then selects a random point within the boundary of each district.

        Attributes
        ----------
        self.districts : list of DetroitDistrict
            The list of district instances in the RedLines class.

        Note
        ----
        The random point is assigned as the randomLat and randomLong  for each district.
        This method assumes the 'self.districts' attribute has been populated with DetroitDistrict instances.

        """
        # Define the grid of points
        xgrid = np.arange(-83.5, -82.8, 0.004)
        ygrid = np.arange(42.1, 42.6, 0.004)
        xmesh, ymesh = np.meshgrid(xgrid, ygrid)
        points = np.vstack((xmesh.flatten(), ymesh.flatten())).T

        for district in self.districts:
        # Ensure the district has valid coordinates
            if not district.coordinates or not isinstance(district.coordinates[0], list):
                print(f"Skipping district {district.id} due to invalid coordinates.")
                continue

            # Flatten the coordinates for the first polygon
            try:
                polygon_coords = np.array(district.coordinates[0][0])  # Extract the outer ring of the first polygon
            except (IndexError, TypeError):
                print(f"Skipping district {district.id} due to invalid polygon structure.")
                continue

            # Create a Path object for the district's first polygon
            polygon_path = Path(polygon_coords)

            # Find points within the polygon
            grid = polygon_path.contains_points(points)
            valid_points = points[grid]

            if len(valid_points) == 0:
                print(f"No valid points found within district {district.id}.")
                district.randomLat = None
                district.randomLong = None
                continue

            # Select a random point from the valid points
            random_point = valid_points[random.choice(range(len(valid_points)))]
            district.randomLong = random_point[0]
            district.randomLat = random_point[1]

            print(f"District {district.id}: Random Point = ({district.randomLat}, {district.randomLong})")

    def fetchCensus(self):
        """
        Fetches the census tract for each district in the list of districts using the FCC API.

        This method iterates over the all districts in `self.districts`, retrieves the census tract
        for each district based on its random latitude and longitude, and updates the district's
        `censusTract` attribute.

        Note
        ----
        The method fetches data from "https://geo.fcc.gov/api/census/area" and assumes that
        `randomLat` and `randomLong` attributes of each district are already set.

        The function `fetch` is an internal helper function that performs the actual API request.

        In the api call, check if the response.status_code is 200.
        If not, it might indicate the api call made is not correct, check your api call parameters.

        If you get status_code 200 and other code alternativly, it could indicate the fcc webiste is not
        stable. Using a while loop to make anther api request in fetch function, until you get the correct result. 

        Important
        -----------
        The order of the API call parameter has to follow the following.
        'lat': xxx,'lon': xxx,'censusYear': xxx,'format': 'json' Or
        'lat': xxx,'lon': xxx,'censusYear': xxx

        """
        base_url = "https://geo.fcc.gov/api/census/area"
        census_year = 2010

        for district in self.districts:
            # Ensure the district has valid randomLat and randomLong
            if district.randomLat is None or district.randomLong is None:
                print(f"Skipping district {district.id} due to missing randomLat or randomLong.")
                district.censusTract = None
                continue

            # Prepare API parameters
            params = {
                'lat': district.randomLat,
                'lon': district.randomLong,
                'censusYear': census_year,
                'format': 'json'
            }

            # Fetch data from the API
            while True:
                try:
                    response = requests.get(base_url, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        if 'results' in data and len(data['results']) > 0:
                            # Extract the census tract code
                            census_tract = data['results'][0].get('block_fips', '')[:9]
                            if len(census_tract) == 9:
                                district.censusTract = census_tract
                                print(f"District {district.id}: Census Tract = {census_tract}")
                            else:
                                print(f"Invalid census tract for district {district.id}.")
                                district.censusTract = None
                            break
                        else:
                            print(f"No results found for district {district.id}. Retrying...")
                    else:
                        print(f"API error for district {district.id}. Status code: {response.status_code}. Retrying...")
                except Exception as e:
                    print(f"Error fetching data for district {district.id}: {e}. Retrying...")

    def fetchIncome(self):

        """
        Retrieves the median household income for each district based on the census tract.

        This method requests income data from the ACS 5-Year Data via the U.S. Census Bureau's API
        for the year 2018. It then maps these incomes to the corresponding census tracts and updates
        the median income attribute of each district in `self.districts`.

        Note
        ----
        The method assumes that the `censusTract` attribute for each district is already set. It updates
        the `medIncome` attribute of each district based on the fetched income data. If the income data
        is not available or is negative, the median income is set to 0.
        """
        base_url = "https://api.census.gov/data/2018/acs/acs5"
        state_fips = "26"  # FIPS code for Michigan
        variables = "B19013_001E"  # Median household income variable

        # Prepare API parameters
        params = {
            "get": f"{variables},NAME",
            "for": "tract:*",
            "in": f"state:{state_fips}"
        }

        try:
            # Fetch data from the Census API
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                # Create a mapping of census tract to median income
                income_data = {}
                for row in data[1:]:  # Skip the header row
                    tract = row[2]  # Census tract
                    income = row[0]  # Median household income
                    try:
                        income = int(income)
                        if income < 0:  # Handle illegal values
                            income = 0
                    except ValueError:
                        income = 0  # Handle non-numeric values
                    income_data[tract] = income

                # Map income data to districts
                for district in self.districts:
                    if district.censusTract in income_data:
                        district.medIncome = income_data[district.censusTract]
                        print(f"District {district.id}: Median Income = {district.medIncome}")
                    else:
                        district.medIncome = 0  # Default to 0 if no data is found
                        print(f"District {district.id}: No income data found. Median Income set to 0.")
            else:
                print(f"Failed to fetch income data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching income data: {e}")

    def cacheData(self, fileName="redlines_cache.json"):
        """
        Saves the current state of district data to a file in JSON format.
        Using the __dict__ magic method on each district instance, and save the 
        result of it to a list.
        After creating the list, dump it to a json file with the inputted name.
        You should name the cache file as redlines_cache.json

        Parameters
        ----------
        filename : str
            The name of the file where the district data will be saved.
        """
        # Create a list of dictionaries representing each district
        district_data = [district.__dict__ for district in self.districts]

        # Write the list to a JSON file
        with open(fileName, 'w') as f:
            json.dump(district_data, f, indent=4)


    def loadCache(self, fileName="redlines_cache.json"):
        """
        Loads district data from a cache JSON file if it exists.

        Parameters
        ----------
        fileName : str
            The name of the file from which to load the district data.
            You should name the cache file as redlines_cache.json

        Returns
        -------
        bool
            True if the data was successfully loaded, False otherwise.
        """
        if not os.path.exists(fileName):
            print(f"Cache file {fileName} does not exist.")
            return False

        try:
            with open(fileName, 'r') as f:
                district_data = json.load(f)

        # Recreate DetroitDistrict instances from the cached data
            self.districts = [DetroitDistrict(**data) for data in district_data]
            print(f"District data successfully loaded from {fileName}.")
            return True
        except Exception as e:
            print(f"Error loading cache file {fileName}: {e}")
            return False

    def calcIncomeStats(self):
        """
        Use np.median and np.mean to
        Calculates the mean and median of median household incomes for each district grade (A, B, C, D).

        This method computes the mean and median incomes for districts grouped by their HOLC grades.
        The results are stored in a list following the pattern: [AMean, AMedian, BMean, BMedian, ...].
        After your calculations, you need to round the result to the closest whole int.
        Relate reading https://www.w3schools.com/python/ref_func_round.asp


        Returns
        -------
        list
            A list containing mean and median income values for each district grade in the order A, B, C, D.
        """
        # Initialize a dictionary to group incomes by HOLC grade
        grade_incomes = {'A': [], 'B': [], 'C': [], 'D': []}

        # Group median incomes by HOLC grade
        for district in self.districts:
            if district.holcGrade in grade_incomes and district.medIncome is not None:
                grade_incomes[district.holcGrade].append(district.medIncome)

        # Calculate mean and median for each grade
        stats = []
        for grade in ['A', 'B', 'C', 'D']:
            incomes = grade_incomes[grade]
            if incomes:
                mean_income = round(np.mean(incomes))
                median_income = round(np.median(incomes))
            else:
                mean_income = 0
                median_income = 0
            stats.extend([mean_income, median_income])

        return stats


    def findCommonWords(self):
         """
        Analyzes the qualitative descriptions of each district category (A, B, C, D) and identifies the
        10 most common words unique to each category.

        This method aggregates the qualitative descriptions for each district category, splits them into
        words, and computes the frequency of each word. It then identifies and returns the 10 most 
        common words that are unique to each category, excluding common English filler words.

        Returns
        -------
        list of lists
            A list containing four lists, each list containing the 10 most common words for each 
            district category (A, B, C, D). The first list should represent grade A, and second for grade B,etc.
            The words should be in the order of their frequency.

        Notes
        -----
        - Common English filler words such as 'the', 'of', 'and', etc., are excluded from the analysis.
        - The method ensures that the common words are unique across the categories, i.e., no word
        appears in more than one category's top 10 list.
        - Regular expressions could be used for word splitting to accurately capture words from the text.
        - Counter from collections could also be used.

        """
        # List of common filler words to exclude
         filler_words = set(['the', 'of', 'and', 'in', 'to', 'a', 'is', 'for', 'on', 'that', 'with', 'as', 'by',
         'it', 'at', 'this', 'an', 'be', 'or', 'from'])

        # Dictionary to store aggregated descriptions by HOLC grade
         grade_descriptions = {'A': '', 'B': '', 'C': '', 'D': ''}

        # Aggregate descriptions for each grade
         for district in self.districts:
            if district.holcGrade in grade_descriptions and district.description:
                grade_descriptions[district.holcGrade] += ' ' + district.description.lower()

        # Dictionary to store unique common words for each grade
         grade_common_words = {'A': [], 'B': [], 'C': [], 'D': []}

        # Compute word frequencies for each grade
         grade_word_counts = {}
         for grade, description in grade_descriptions.items():
            # Split description into words using regex and filter out filler words
            words = re.findall(r'\b\w+\b', description)
            filtered_words = [word for word in words if word not in filler_words]
            # Count word frequencies
            grade_word_counts[grade] = Counter(filtered_words)

        # Identify unique common words for each grade
         for grade in ['A', 'B', 'C', 'D']:
            # Get the 10 most common words for the current grade
            most_common = grade_word_counts[grade].most_common(10)
            # Extract only the words
            grade_common_words[grade] = [word for word, _ in most_common]

        # Ensure words are unique across grades
         unique_words = {'A': set(grade_common_words['A']),
                        'B': set(grade_common_words['B']),
                        'C': set(grade_common_words['C']),
                        'D': set(grade_common_words['D'])}

         for grade in ['A', 'B', 'C', 'D']:
            other_grades = {'A', 'B', 'C', 'D'} - {grade}
            for other_grade in other_grades:
                unique_words[grade] -= unique_words[other_grade]

        # Convert unique words back to lists and limit to 10 words
         for grade in ['A', 'B', 'C', 'D']:
            grade_common_words[grade] = list(unique_words[grade])[:10]

        # Return the results as a list of lists
         return [grade_common_words['A'], grade_common_words['B'], grade_common_words['C'], grade_common_words['D']]

    def calcRank(self):
        """
        Calculates and assigns a rank to each district based on median income.

        This method sorts the districts in descending order of their median income and then assigns
        a rank to each district, with 1 being the highest income district.

        Note
        ----
        The rank is assigned based on the position in the sorted list, so the district with the highest
        median income gets a rank of 1, the second-highest gets 2, and so on. Ties are not accounted for;
        each district will receive a unique rank.

        Important:
        If you do the extra credit, you need to edit the __init__ of DetroitDistrict adding another arg "rank" with
        default value to be None. Not doing so might cause the load cache method to fail if you use the ** operator in load cache. 

        Attribute
        ----
        rank

        """


        pass

    def calcPopu(self):
        """
        Fetches and calculates the percentage of Black or African American residents in each district.

        This method fetch the total and Black populations for each census tract in Michigan from
        the U.S. Census Bureau's API, like the median income data.  It then calculates the percentage of Black residents in each tract
        and assigns this value to the corresponding district percent attribute.

        Note
        ----
        The method assumes that the census tract IDs in the district data match those used by the Census Bureau.
        The percentage is rounded to two decimal places. If the Black population is zero, the percentage is set to 0.
        Elif the total population is zero, the percentage is set to 1.

        Important:
        If you do the extra credit, you need to edit the __init__ of DetroitDistrict adding another arg "percent" with
        default value to be None. Not doing so might cause the load cache method to fail if you use the ** operator in load cache.


        Attribute
        ----
        percent

        """
        pass


    def comment(self):
        '''
        Look at the
        districts in each category, A, B, C and D. Are there any trends that you see? Share 1 paragraph of your
        findings. And a few sentences(more than 50 words) about how this exercise did or did not change your understanding of
        residential segregation. Print you thought in the method.
        '''
        print("")


# Use main function to test your class implementations.
# Feel free to modify the example main function.
def main():
    myRedLines = RedLines()
    myRedLines.createDistricts('redlines_data.json')
    myRedLines.plotDistricts()
    myRedLines.generateRandPoint()
    myRedLines.fetchCensus()
    myRedLines.fetchIncome()
    myRedLines.cacheData('redlines_cache.json')
    myRedLines.loadCache('redlines_cache.json')

if __name__ == '__main__':
    main()



