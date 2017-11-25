#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <array>
#include <map>
#include <algorithm>
#include <omp.h>
#include <time.h>
using namespace std;

vector< array<string, 2> > FORMULA;

void formula(int x, int y, string archivo);
string coeficiente(array<string, 2> formula1, array<string, 2> formula2);
float calculojt(array<string, 2> formula1, array<string, 2> formula2);
map<char, int> comparador(string formula);

int main() {
  
   string cadena, id, compuesto;

   ifstream fe("ZINC_chemicals1.tsv");

   while(getline(fe, cadena)) {
       istringstream stream(cadena);
       stream >> id >> compuesto;
       array<string, 2> fila{id, compuesto};
       FORMULA.push_back(fila);
   }
   fe.close();
   vector< vector<string> > listas;
   listas.resize(4);
   int limites[] = {0, 6073, 8588, 10518, 12144};
   string archivos[] = {"archivo1.tsv","archivo1.tsv","archivo1.tsv","archivo1.tsv"};
   #pragma omp parallel num_threads(4)
   {
       int pid = omp_get_thread_num();
       formula(limites[pid], limites[pid+1], archivos[pid]);
   }
      
  
   
   
   
   return 0;
}

void formula(int x, int y, string formula){
   clock_t t_start, t_end;
   double secs;
 ofstream salida1(formula, ofstream::out);   

for (int i =0; i < y; i++){
        for (int j=i+1; j<y;j++ ){
            salida1 << coeficiente(FORMULA[i], FORMULA[j]);
       

           t_end = clock();
           secs= (double) (t_end - t_start) / CLOCKS_PER_SEC;
          

     }
    }
printf("%.g \n" , secs);

}

string coeficiente(array<string, 2> formula1, array<string, 2> formula2){
    string elemento;
    float val = calculojt(formula1, formula2);
    stringstream ss (stringstream::in | stringstream::out);
    ss << val;
    elemento = formula1[0] + "\t" + formula2[0] + "\t" + ss.str() +"\n";
    return elemento;
}

float calculojt(array<string, 2> formula1, array<string, 2> formula2){
    map<char, int> diccionario1;
    map<char, int> diccionario2;
    map<char, int> diccionario3;
    int na =0;
    int nb =0;
    int nc =0;
    int a = 0; 
    int b = 0; 
    int comun = 0; 
    float coefjt=0;
    diccionario1 = comparador(formula1[1]);
    diccionario2 = comparador(formula2[1]); 
    for (auto &c : diccionario1){
        if (diccionario2.count(c.first) > 0){
            a=diccionario1[c.first];
            b=diccionario2[c.first];
            comun=min(a,b);
            diccionario3[c.first] = comun;
        }
    }
    for (auto &c : diccionario1){
        na += diccionario1[c.first];
    }
    for (auto &c : diccionario2){
        nb += diccionario2[c.first];
    }
    for (auto &c : diccionario3){
        nc += diccionario3[c.first];
    }
    coefjt = nc / (float) (na + nb - nc);
    int h = 100*coefjt;
    coefjt = h*1.0/100;
   
    return coefjt;
}

map<char, int> comparador(string formula){
    map<char, int> diccionario;
    for (char &c : formula){
        if( c == '@'){
            diccionario[c] = 1;
        }
        else if(diccionario.count(c) > 0 ){
            diccionario[c]++;
        }
        else {
            diccionario[c] = 1;
        }
    }
    return diccionario;
}

