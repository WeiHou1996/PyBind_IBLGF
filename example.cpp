#include <pybind11/pybind11.h>
#include <vector>
#include <bits/stdc++.h>
#include <pybind11/stl.h>

#include <iostream>
#include <pybind11/operators.h>

#include "./sparse_mat.hpp"

namespace py = pybind11;

struct Pet {
    Pet(const std::string &name) : name(name) { }
    std::string name;
};

struct Dog : Pet {
    Dog(const std::string &name) : Pet(name) { }
    std::string bark() const { return "woof!"; }
};

template <typename T>
struct VecPet {
	VecPet() = default;
	VecPet(const T& ele, size_t n) {
		for (size_t i = 0; i < n; ++i) {
			names.push_back(ele);
		}
	}
	std::vector<T> names;
};



PYBIND11_MODULE(example, m){
	py::class_<Pet>(m, "Pet")
	.def(py::init<const std::string &>())
	.def_readwrite("name", &Pet::name);

	// Method 1: template parameter:
	py::class_<Dog, Pet /* <- specify C++ parent type */>(m, "Dog")
		.def(py::init<const std::string &>())
		.def("bark", &Dog::bark);

	py::class_<VecPet<Pet>>(m, "VecPet")
		.def(py::init())
		.def(py::init<const Pet &, size_t>())
		.def_readwrite("names", &VecPet<Pet>::names);

	py::class_<VecPet<Dog>>(m, "VecDog")
		.def(py::init())
		.def(py::init<const Dog &, size_t>())
		.def_readwrite("names", &VecPet<Dog>::names);

	py::class_<sparse_mat<double>>(m, "sparse_mat")
		.def(py::init())
		.def(py::self + py::self)
		.def("print_row", &sparse_mat<double>::print_row)
		.def("print_row_full", static_cast<void (sparse_mat<double>::*)(int)>(&sparse_mat<double>::print_row_full))
		.def("print_row_full", static_cast<void (sparse_mat<double>::*)(int, size_t)>(&sparse_mat<double>::print_row_full))
		.def("numRow_loc", &sparse_mat<double>::numRow_loc)
		.def("add_element", &sparse_mat<double>::add_element)
		.def("resizing_row", &sparse_mat<double>::resizing_row)
		.def("get_CSR", [](sparse_mat<double>* self) {
			size_t s = self->tot_size(false);
			size_t n_rows = self->numRow_loc();
			std::vector<double> a(s,0);
			std::vector<int> ia(n_rows+1,0), ja(s,0);
			
			self->template getCSR_zero_begin(ia.data(), ja.data(), a.data());
			return std::tuple<std::vector<int>, std::vector<int>, std::vector<double>>{ia, ja, a};
		});
}
