// DSQSS (Discrete Space Quantum Systems Solver)
// Copyright (C) 2018- The University of Tokyo
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

#ifndef SRC_COMMON_TOSTRING_H_
#define SRC_COMMON_TOSTRING_H_

#include <sstream>
#include <string>

template <class T>
std::string tostring(T const& x) {
  std::stringstream ss;
  ss << x;
  return ss.str();
}

#endif  // SRC_COMMON_TOSTRING_H_
