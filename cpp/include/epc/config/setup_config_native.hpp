#pragma once
#ifndef EPC_CONFIG_SETUP_CONFIG_NATIVE_HPP_INCLUDE
#define EPC_CONFIG_SETUP_CONFIG_NATIVE_HPP_INCLUDE

#include "Empirical/include/emp/config/ArgManager.hpp"

#include "try_read_config_file.hpp"

namespace epc {

void setup_config_native(epc::Config & config, int argc, char* argv[]) {
  auto specs = emp::ArgManager::make_builtin_specs(&config);
  emp::ArgManager am(argc, argv, specs);
  epc::try_read_config_file(config, am);
}

} // namespace epc

#endif // #ifndef EPC_CONFIG_SETUP_CONFIG_NATIVE_HPP_INCLUDE
