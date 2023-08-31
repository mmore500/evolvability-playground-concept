#pragma once
#ifndef EPC_CONFIG_TRY_READ_CONFIG_FILE_HPP_INCLUDE
#define EPC_CONFIG_TRY_READ_CONFIG_FILE_HPP_INCLUDE

#include <cstdlib>
#include <filesystem>
#include <iostream>

#include "Config.hpp"

namespace epc {

void try_read_config_file(epc::Config & config, emp::ArgManager & am) {
  if(std::filesystem::exists("epc.cfg")) {
    std::cout << "Configuration read from epc.cfg" << '\n';
    config.Read("epc.cfg");
  }
  am.UseCallbacks();
  if (am.HasUnused())
    std::exit(EXIT_FAILURE);
}

} // namespace epc

#endif // #ifndef EPC_CONFIG_TRY_READ_CONFIG_FILE_HPP_INCLUDE
