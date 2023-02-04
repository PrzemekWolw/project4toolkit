#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <regex>
#include <map>
#include <string>
#include <array>

class Vertex {
 public:
  int index = 0;
  std::vector<float> coordinates = {0, 0, 0};
  std::vector<float> normal = {0, 0, 0};
  std::vector<float> uv = {0, 0, 0};

  Vertex(int index, std::vector<float> coordinates, std::vector<float> normal,
         std::vector<float> uv)
      : index(index),
        coordinates(coordinates),
        normal(normal),
        uv(uv) {}

  std::string get_v() {
    std::stringstream ss;
    ss << "v ";
    for (int i = 0; i < coordinates.size(); i++) {
      ss << coordinates[i] << " ";
    }
    return ss.str();
  }

  std::string get_vn() {
    std::stringstream ss;
    ss << "vn ";
    for (int i = 0; i < normal.size(); i++) {
      ss << normal[i] << " ";
    }
    return ss.str();
  }

  std::string get_vt() {
    std::stringstream ss;
    ss << "vt ";
    for (int i = 0; i < uv.size(); i++) {
      ss << uv[i] << " ";
    }
    return ss.str();
  }

  int get_index() { return index; }
};

class Face {
 public:
  std::vector<Vertex*> vertices;

  Face(std::vector<Vertex*> vertices) : vertices(vertices) {}

  std::string get_f() {
    std::stringstream ss;
    ss << "f ";
    for (int i = 0; i < vertices.size(); i++) {
      ss << vertices[i]->get_index() + 1 << "/"
         << vertices[i]->get_index() + 1 << "/"
         << vertices[i]->get_index() + 1 << " ";
    }
    return ss.str();
  }
};

class Mesh {
  int index;
  int vertex_offset;
  std::vector<int> idx_data;
  std::vector<std::string> vert_data;

  std::vector<Vertex> vertices;
  std::vector<Face> faces;
  Material *material = nullptr;

public:
  Mesh(int index) : index(index), vertex_offset(0) {}

  void set_vertex_offset(int vertex_offset) { this->vertex_offset = vertex_offset; }

  void add_idx(std::vector<int> data) {
    for (int id : data) {
      this->idx_data.push_back(id);
    }
  }

  void add_vert(std::string data) { this->vert_data.push_back(data); }

  void generate() {
    int vert_index = this->vertex_offset;

    for (std::string raw_vert : this->vert_data) {
      std::vector<std::string> coord = split_string(raw_vert.substr(0, raw_vert.find(" / ")), " ");
      for (int i = 0; i < coord.size(); i++) {
        coord[i] = std::stof(coord[i]);
      }

      std::vector<std::string> normal = split_string(raw_vert.substr(raw_vert.find(" / ") + 3, raw_vert.rfind(" / ")), " ");
      for (int i = 0; i < normal.size(); i++) {
        normal[i] = std::stof(normal[i]);
      }

      std::vector<std::string> uv = split_string(raw_vert.substr(raw_vert.rfind(" / ") + 3), " ");
      if (uv.size() != 2) {
        uv = split_string(raw_vert.substr(raw_vert.rfind(" / " + 3, raw_vert.rfind(" / ") - 3)), " ");
      }
      uv[0] = std::stof(uv[0]);
      uv[1] = -std::stof(uv[1]);

      Vertex vertex(vert_index, coord, normal, uv);
      this->vertices.push_back(vertex);
      vert_index++;
    }

    for (int i = 0; i < this->idx_data.size(); i += 3) {
      Vertex v1 = this->vertices[this->idx_data[i]];
      Vertex v2 = this->vertices[this->idx_data[i + 1]];
      Vertex v3 = this->vertices[this->idx_data[i + 2]];

      Face face({v1, v2, v3});
      this->faces.push_back(face);
    }
  }
};

class Material {
public:
  std::string name = "";
  std::array<float, 3> Ka = {0, 0, 0};
  std::array<float, 3> Kd = {0, 0, 0};
  std::array<float, 3> Ks = {0, 0, 0};
  float Ns = 0;
  float Ni = 0;
  float d = 0;
  int illum = 0;
  std::string map_Kd = "";
  std::string map_bump = "";
  std::string map_Ks = "";

  Material(std::string name) {
    this->name = name;
    Ka = {0, 0, 0};
    Kd = {0, 0, 0};
    Ks = {0, 0, 0};
    Ns = 0;
    Ni = 0;
    d = 0;
    illum = 0;
    map_Kd = "";
    map_bump = "";
    map_Ks = "";
  }

  std::string generate() {
    if (name.empty()) {
      return "";
    }

    std::string mtl = "";
    mtl += "newmtl " + name + "\n";
    if (!map_Kd.empty()) {
      mtl += "map_Kd " + map_Kd + "\n";
    }
    if (!map_bump.empty()) {
      mtl += "map_bump " + map_bump + "\n";
    }
    if (!map_Ks.empty()) {
      mtl += "map_Ks " + map_Ks + "\n";
    }
    mtl += "\n";
    return mtl;
  }
};

class MaterialParser {
public:
    std::vector<Material> shaders;

    MaterialParser(const std::vector<std::string>& raw_shader_list) {
        shaders = std::vector<Material>();
        for (int index = 0; index < raw_shader_list.size(); ++index) {
            Material material = Material(("MAT_" + std::to_string(index)).c_str());
            material.map_Kd = raw_shader_list[index];
            shaders.push_back(material);
        }
    }

    std::vector<Material> generate() {
        return shaders;
    }
};

