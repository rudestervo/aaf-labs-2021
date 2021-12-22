### Бригада
* Плахтій Гліб ФІ-92
* Шевцова Марія ФІ-92

### Варіант
Варіант №10: Множина точок у двовимірній декартовій площині (R-Tree)

### Графік
* реалізація R-tree (Insert, Search)
	**04.10.2021**
* Реалізація парсера
	**01.11.2021**
* Обробка всіх помилок та фінальний вигляд роботи
	**29.11.2021**



# Visualization R-Tree structure and colmpile R-Tree as python library:
### compilation
to compile R-Tree as python library you shoukd **for Linux**:
1) clone [pybind11](https://github.com/pybind/pybind11.git) into R_Tree_to_compile folder  
> **git clone** https://github.com/pybind/pybind11.git
2) crate directory **build** in R_tree_to_compile folder  
> **mkdir build**  
> **cd build**  
3) compile R_Tree scripts using CMake:   
> **cmake ..**  
> **make** 

then you get a R-Tree.\*.os file in build folder which you can import in python  
### visualization
![visulisation](https://github.com/GlebPlakhtii/aaf-labs-2021/blob/master/plakhtii_fi-92_shevtsova_fi-92/visualisation.jpg)  
* **to create a new rect you shold left mouse click to start drawing and left left click to finish**  
* **to change inset/search click S key**







