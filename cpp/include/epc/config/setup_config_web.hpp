#pragma once
#ifndef EPC_CONFIG_SETUP_CONFIG_WEB_HPP_INCLUDE
#define EPC_CONFIG_SETUP_CONFIG_WEB_HPP_INCLUDE

#include "Empirical/include/emp/config/ArgManager.hpp"
#include "Empirical/include/emp/web/UrlParams.hpp"
#include "Empirical/include/emp/web/web.hpp"

#include "Config.hpp"
#include "try_read_config_file.hpp"

namespace epc {

void setup_config_web(epc::Config & config)  {
  auto specs = emp::ArgManager::make_builtin_specs(&config);
  emp::ArgManager am(emp::web::GetUrlParams(), specs);
  epc::try_read_config_file(config, am);
}

} // namespace epc

#endif // #ifndef EPC_CONFIG_SETUP_CONFIG_WEB_HPP_INCLUDE
