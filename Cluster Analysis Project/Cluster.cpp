#include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <limits>

//Parent of Data class
/*Description: This class is used for cluster centroids asd is the paraent and friend class for data points. This class contains members
               for the floating Point values of the x and y coordinates of the data points and centroids.
*/
class Point{
  private:
      float x;
      float y;
  public:
      Point();
      Point(float x, float y);
      void display();
      float get_x();
      float get_y();
      void set_x(float);
      void set_y(float);
      friend class Data;
};

//Chile of Point class
/*Description: This class is used for data points. This class inherits from the Point class and adds an additional member for
*/
class Data: public Point{
  private:
      int cluster;
  public:
      Data();
      Data(float x, float y);
      void set_cluster(int cluster);
      int get_cluster();
      void display();
};

/*Description: Sets the value of the x coordinate of a Point or Data
  PreConditions: Class object must already be initialize and a float must be given as a parameter
  PostConditions: The x member of the class object is changed to the float value given in the parameter
*/
void Point::set_x(float x){
  this->x = x;
}

/*Description: Sets the value of the y coordinate of a Point or Data
  PreConditions: Class object must already be initialize and a float must be given as a parameter
  PostConditions: The y member of the class object is changed to the float value given in the parameter
*/
void Point::set_y(float y){
  this->y = y;
}

/*Description: Returns the cluster index of a Data object from 0 to ((Number of Clusters) - 1). The index is cluster_index
               so that the return value can be used to access the centroid a cluster in the centroid vector
 *PreConditions: Object has been initialized and assigned a cluster
 *PostConditions: Returns the cluster index number
*/
int Data::get_cluster(){
  return this->cluster;
}

/*Description: Returns the x coordinate of Point or Data member
 *PreConditions: Object has been initialized and assigned an x coordinate
 *PostConditions: Returns the x coordinate
*/
float Point::get_x(){
  return this->x;
}

/*Description: Returns the y coordinate of Point or Data member
 *PreConditions: Object has been initialized and assigned an y coordinate
 *PostConditions: Returns the y coordinate
*/
float Point::get_y(){
  return this->y;
}

/*Description: Sets the value of the assigned cluster of a Data object
  PreConditions: Class object must already be initialize and an int from 0 to ((Number of clusters) - 1) must be given as a parameter
  PostConditions: The cluster member of the class object is changed to the int value given in the parameter
*/
void Data::set_cluster(int cluster){
  this->cluster = cluster;
}

/*Description: Displays the x and y coordinate information for a Point object
 *PreConditions: Class object must be initialized and coordinate values must be set
 *PostConditions: X and Y coordinates will be printed to the command line
*/
void Point::display(){
  std::cout << "X: " << this->x << "\tY: " << this->y << std::endl;
}

/*Description: Displays the x and y coordinate information as well as the cluster assignment for a Data object
 *PreConditions: Class object must be initialized. The coordinate and cluster values must be set
 *PostConditions: X and Y coordinates and the cluster assignment of the object will be printed to the command line
*/
void Data::display(){
  std::cout << "X: " << this->x << "\tY: " << this->y << "\tCentroid: "<< this->cluster + 1 << std::endl;
}

/*Description: Default constructor for the Point class
 *PreConditions: None
 *PostConditions: The object is created. X and y coordinate members of the Point class are set to 0
*/
Point::Point(){
  this->x = 0;
  this->y = 0;
}

/*Description: Default constructor for the Data class
 *PreConditions: None
 *PostConditions: The object is created. X and y coordinate members of the Data class are set to 0. The cluster assignment is also set to 0
*/
Data::Data():Point(){
  this->cluster = 0;
}

/*Description: Constructor for the Point class
 *PreConditions: Two floating point values are given as parameters
 *PostConditions: The object is created with the X and Y members set to the x and y parameter values.
*/
Point::Point(float x, float y){
  this->x = x;
  this->y = y;
}

/*Description: Constructor for the Data class
 *PreConditions: Two floating point values are given as parameters
 *PostConditions: The object is created with the X and Y members set to the x and y parameter values. The cluster assignment is set to 0
*/
Data::Data(float x, float y):Point(x, y){
  this->cluster = 0;
}

/*Description: Calulated the distance between a Data object data point and the Point object centroid.
 *PreConditions: Valid initialized Data and Point objects are given as parameters
 *PostConditions: The distance between the two objects based on their x and y coordinates is returned as a float
*/
float distance(Data data_point, Point centroid){
  float dx, dy;
  //Calculate the distance betweent the x and y values of the two points
  dx = abs(data_point.get_x() - centroid.get_x());
  dy = abs(data_point.get_y() - centroid.get_y());
  float distance = sqrt( pow(dx, 2) + pow(dy, 2) );
  return distance;
}

/*Description: This function will assign clusters to each data point based on their distance to each centroid
 *PreConditions: Point centroids adnd Data need to have valid x and y coordinates a
 *PostConditions: The cluster member of each data point will be given the index the closest cluster
*/
void assign_cluster(std::vector<Data> &data_points, std::vector<Point> centroids){
  float min, test_min;  //variables to track the min distance from a centroid to a data point and a variable to track the distance being tested
  //loop through each data point
  for (int d = 0; d < data_points.size(); d++) {
    min = std::numeric_limits<float>::max();  //initialize the overall min variable to be the minimum possible float value
    //loop through each centroid
    for (int c = 0; c < centroids.size(); c++) {
      test_min = distance(data_points[d], centroids[c]); //Calulate the distance from the given centroid the given point
      //if the minimum being tested is less than the overall min then update its value and set the cluster of the data to the cluster index
      if(test_min < min){
        min = test_min;
        data_points[d].set_cluster(c);
      }
    }
  }
}

/*Description: Updates the centroids of eachc cluster coordinates by calculating the average x and y values of
               each data point assigned to each cluster
 *PreConditions: Data points have already been assigned to the closest cluster
 *PostConditions: the centroids of each cluster will have updated values
*/
void update_centroids(std::vector<Data> data_points, std::vector<Point> &centroids){
  //vectors for count of each data point assigned to each clusters and the sum of the
  //x and y coordinates for each data point assigned to each cluster
  std::vector<float> centroid_count(centroids.size());
  std::vector<float> centroid_x_sum(centroids.size());
  std::vector<float> centroid_y_sum(centroids.size());

  int cluster_index; //variable to get the cluster assigned to each data point
  //loop through each data point
  for(int n = 0; n < data_points.size(); n++){
    cluster_index = data_points[n].get_cluster(); //get the cluster index assigned to the data point
    centroid_count[cluster_index]++;  //increment the count for the given cluster
    centroid_x_sum[cluster_index] += data_points[n].get_x();  //add the value of the x coordinate to the sum for the given cluster
    centroid_y_sum[cluster_index] += data_points[n].get_y();  //add the value of the y coordinate to the sum for the given cluster
  }
  //loop for each cluster centroid
  for(int v = 0; v < centroids.size(); v++){
    //calculate the average of the x coordinates and store as the new x coordinate for the cluster centroid
    centroids[v].set_x( (float) ((centroid_x_sum[v]) / (centroid_count[v])) );
    //calculate the average of the y coordinates and store as the new y coordinate for the cluster centroid
    centroids[v].set_y( (float) ((centroid_y_sum[v]) / (centroid_count[v])) );
  }
}

/*Description: Loads data from infile and stores the x and y value as a data point
 *PreConditions: Each x and y coordinate is seperated by a space and the ifstream for a valid read file is opened and given in parameter
 *PostConditions: A vector of data points is generated
*/
std::vector<Data> load_data(std::ifstream& infile){
  float buffer, temp_x, temp_y; //buffer stores read variable, temp x and y store values stored in buffer
  Data temp;
  std::vector<Data> data_points;
  bool x = true;  //variable to track whether the value being read in is an x value or y value
  //loop while values are still being read from the infile
  while(infile >> buffer){
    if(x){
      temp_x = buffer;
    }else{
      temp_y = buffer;              //in this instance temp_y is not needed but makes what the func. is doing more clear
      temp = Data(temp_x, temp_y);  //create the Data object
      data_points.push_back(temp);  //add the Data object to the data point vector
    }
    x = !x; //change the variable of whether the input is x or y to the opposite of what it already is
  }
  return data_points; //return the vector of loaded data points
}

/*Description:
 *PreConditions
 *PostConditions:
*/
std::vector<Point> generate_centroids(int n_clusters, std::vector<Data> data_points){
  srand(time(NULL));
  std::vector<Point> centroids(n_clusters);
  std::vector<int> cluster_indices(n_clusters);
  int index;
  bool contains;
  Data temp_data_point;
  Point centroid;
  for(int n = 0; n < n_clusters; n++){
    do{
      contains = false;
      index = rand() % data_points.size();
      for(int i = 0; i < cluster_indices.size(); i++){
          if(index == cluster_indices[i]){
            contains = true;
          }
      }
    }while(contains == true);
    cluster_indices[n] = index;
    centroid = Point(data_points[index].get_x(), data_points[index].get_y());
    centroids[n] = centroid;
  }
  return centroids;
}

/*Description: Funtion to tell whether a vector of points is equal
 *PreConditions: Two valid and initialized Point vectors are given in parameter. Vectors must also be the same size
 *PostConditions: Returns a boolean of whether the vectors have all equal x and y coordinates
*/
bool equal(std::vector<Point> current, std::vector<Point> prev){
  //loops through all Points in the vector
  for(int n = 0; n < current.size(); n++){
    //if either the x or y values are different return false
    if( (current[n].get_x() != prev[n].get_x()) || (current[n].get_y() != prev[n].get_y()) ){
      return false;
    }
  }
  return true;  //if the function exits the for loop without returning false then the vecotrs are equal and we return true
}

/*Description: Main function for the program
*/
int main(int argc, char const *argv[]) {

  //open the data file for reading only
  std::ifstream infile;
  infile.open("C:/Users/Richard/Desktop/data.txt");
  if(infile.fail())
    std::cout << "Failed to load data" << '\n';

  //load the data from the infile
  std::vector<Data> data_points = load_data(infile);
  infile.close();

  //prompt the user for the number of clusters to create and generate the centroids
  int n_clusters;
  std::cout << "How many clusters would you like to generate?\nNumber of Clusters: ";
  std::cin >> n_clusters;
  std::vector<Point> centroids = generate_centroids(n_clusters, data_points);

  //Print the values of the intially choosen centroids
  std::cout << "\nInitial Centroids: " << std::endl;
  for (int n = 0; n < centroids.size(); n++) {
    centroids[n].display();
  }

  //create a vector that will save precious centroid values
  std::vector<Point> prev_centroids(centroids.size());

  //loop until the values of the centroids doesn't change from the previous
  do{
    prev_centroids = centroids;               //save the current centroids as previous centroids
    assign_cluster(data_points, centroids);   //assign cluster values to each data points
    update_centroids(data_points, centroids); //update the centroid values
  }while(!equal(centroids, prev_centroids));

  //print the final values of the centroids
  std::cout << "\nFinal Centroids: " << std::endl;
  for (int x = 0; x < centroids.size(); x++) {
    centroids[x].display();
  }

  //Print the final values of the data points and their cluster assignments
  std::cout << "\nData Points Assignments: " << std::endl;
  for (int y = 0; y < data_points.size(); y++) {
    data_points[y].display();
  }

  //Conclude the program
  return 0;
}
