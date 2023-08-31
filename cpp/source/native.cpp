#include <iostream>

#include "Empirical/include/emp/base/vector.hpp"

#include "epc/config/Config.hpp"
#include "epc/config/setup_config_native.hpp"
#include "epc/example.hpp"

// This is the main function for the NATIVE version of Evolvability Playground Concept.

epc::Config cfg;

int main(int argc, char* argv[]) {
  // Set up a configuration panel for native application
  setup_config_native(cfg, argc, argv);
  cfg.Write(std::cout);

  std::cout << "Hello, world!" << "\n";

  return epc::example();
}
