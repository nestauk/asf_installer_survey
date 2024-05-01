# Checking variable
check_variable <- function(var, ids) {
  map(ids, \(x) {
    print(x)
    data |>
      filter(x0a_response_id == x) |>
      select(.data[[var]]) |>
      as.data.frame()
  })
}

# Recoding
recode_variable <- function(var, ids, replace_with) {
  data |>
    mutate(!!as.name(var) := ifelse(
      x0a_response_id %in% ids,
      replace_with,
      .data[[var]]
    ))
}

# Recoding factor
recode_factor_existing <- function(var, ids, replace_with) {
  levels <- data |>
    pull(.data[[var]]) |>
    levels()  
  
  data |>
    mutate(!!as.name(var) := factor(
      case_when(
        x0a_response_id %in% ids ~ replace_with,
        TRUE ~ .data[[var]]
      ),
      levels = levels))
}

# Recoding factor with new level
recode_factor_new <- function(var, ids, replace_with) {
  levels <- data |>
    pull(.data[[var]]) |>
    levels()  
  
  levels <- c(levels, replace_with)
  
  data |>
    mutate(!!as.name(var) := factor(
      case_when(
        x0a_response_id %in% ids ~ replace_with,
        TRUE ~ .data[[var]]
      ),
      levels = levels))
}

# Replacing
replace_variable <- function(var, ids, replace_with) {
  data |>
    mutate(!!as.name(var) := ifelse(
      x0a_response_id %in% ids,
      map(
        .data[[var]],
        \(x) {
          replace(x, x == "Other", replace_with)
        }),
      .data[[var]]
    ))
}

# Q16a
var <- "x16a_what_types_of_heat_pump_has_your_company_installed_over_the_last_12_months_select_all_that_apply"
ids <- c(451, 489, 595, 604)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# Q16b

var <- "x16b_what_types_of_heat_pump_have_you_installed_over_the_last_12_months_select_all_that_apply"
ids <- c(151, 594, 675, 781)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# 17a

var <- "x17a_what_type_of_heat_pump_has_your_company_installed_most_often_over_the_last_12_months_please_select_one_option"
ids <- c(451, 489, 595, 604)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_factor_new(var, ids, replace_with)
check_variable(var, ids)


# 17b

var <- "x17b_what_type_of_heat_pump_have_you_installed_most_often_over_the_last_12_months_please_select_one_option"
ids <- c(213, 594, 810)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_factor_new(var, ids, replace_with)
check_variable(var, ids)



var <- "x25b_why_arent_you_mcs_certified_select_all_that_apply"
ids <- c(594)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)



var <- "x25c_why_arent_you_mcs_certified_select_all_that_apply"
ids <- c(810)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)



var <- "x29_why_do_you_prefer_to_remain_without_mcs_certification_select_all_that_apply"
ids <- c(151, 430)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# 31a 1

var <- "x31a_over_the_past_12_months_has_your_business_done_retrofit_heat_pump_installations_in_any_of_the_following_properties_select_all_that_apply"
ids <- c(90, 607)
replace_with <- "Individual private homes"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# 31a 2

var <- "x31a_over_the_past_12_months_has_your_business_done_retrofit_heat_pump_installations_in_any_of_the_following_properties_select_all_that_apply"
ids <- c(451, 489, 595, 604, 837)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# 31a 3

var <- "x31a_over_the_past_12_months_has_your_business_done_retrofit_heat_pump_installations_in_any_of_the_following_properties_select_all_that_apply"
ids <- c(346)
replace_with <- "Other - not relevant"

print(var)
check_variable(var, ids)
data <- replace_variable(var, ids, replace_with)
check_variable(var, ids)


# 31b 1

var <- "x31b_over_the_past_12_months_have_you_done_retrofit_heat_pump_installations_in_any_of_the_following_properties_select_all_that_apply"
ids <- c(594, 781, 810)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# 31b 2

var <- "x31b_over_the_past_12_months_have_you_done_retrofit_heat_pump_installations_in_any_of_the_following_properties_select_all_that_apply"
ids <- c(188)
replace_with <- "Social housing"

print(var)
check_variable(var, ids)
data <- replace_variable(var, ids, replace_with)
check_variable(var, ids)


# 32a

var <- "x32a_over_the_past_12_months_has_your_business_done_any_new_build_heat_pump_installations_in_any_of_the_following_properties_select_all_that_apply"
ids <- c(489, 595)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# 32b

var <- "x32b_over_the_past_12_months_have_you_done_any_new_build_heat_pump_installations_in_any_of_the_following_properties_select_all_that_apply"
ids <- c(781)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# 34a

var <- "x34a_over_the_past_12_months_which_of_the_following_accounts_for_the_majority_of_the_retrofit_heat_pump_installations_your_business_has_done"
ids <- c(451, 489, 595, 604, 837)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_factor_new(var, ids, replace_with)
check_variable(var, ids)


# 34b

var <- "x34b_over_the_past_12_months_which_of_the_following_accounts_for_the_majority_of_your_retrofit_heat_pump_installations"
ids <- c(810)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_factor_new(var, ids, replace_with)
check_variable(var, ids)


# 35a

var <- "x35a_over_the_past_12_months_which_of_the_following_accounts_for_the_majority_of_the_new_build_heat_pump_installations_your_business_has_done"
ids <- c(489, 595)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_factor_new(var, ids, replace_with)
check_variable(var, ids)

# 36a 1

var <- "x36a_in_your_businesss_retrofit_work_does_your_business_install_heat_pumps_through_select_all_that_apply"
ids <- c(451, 489, 604)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# 36a 2

var <- "x36a_in_your_businesss_retrofit_work_does_your_business_install_heat_pumps_through_select_all_that_apply"
ids <- c(365)
replace_with <- "Other - not relevant"

print(var)
check_variable(var, ids)
data <- replace_variable(var, ids, replace_with)
check_variable(var, ids)


# 36b 1

var <- "x36b_in_your_retrofit_work_do_you_install_heat_pumps_through_select_all_that_apply"
ids <- c(410, 594)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# 36b 2

var <- "x36b_in_your_retrofit_work_do_you_install_heat_pumps_through_select_all_that_apply"
ids <- c(659)
replace_with <- "Other - not relevant"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# 36c

var <- "x36c_in_your_retrofit_work_do_you_install_heat_pumps_through_select_all_that_apply"
ids <- c(781)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# 36d

var <- "x36d_in_your_retrofit_work_do_you_install_heat_pumps_through_select_all_that_apply"
ids <- c(810)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


# 40a 1

var <- "x40a_whats_the_biggest_barrier_to_you_installing_more_heat_pumps_please_select_one_option"
ids <- c(186, 192, 270, 366)
replace_with <- "I have too little customer demand"

print(var)
check_variable(var, ids)
data <- recode_factor_existing(var, ids, replace_with)
check_variable(var, ids)


# 40a 2

var <- "x40a_whats_the_biggest_barrier_to_you_installing_more_heat_pumps_please_select_one_option"
ids <- c(77, 168, 413)
replace_with <- "I find that ‘unnecessary’ elements of installation or admin take up so much time that my business is prevented from doing more jobs"

print(var)
check_variable(var, ids)
data <- recode_factor_existing(var, ids, replace_with)
check_variable(var, ids)


# 40a 3

var <- "x40a_whats_the_biggest_barrier_to_you_installing_more_heat_pumps_please_select_one_option"
ids <- c(412, 515, 672)
replace_with <- "I am unable to find additional suitable staff"

print(var)
check_variable(var, ids)
data <- recode_factor_existing(var, ids, replace_with)
check_variable(var, ids)

# 40a 4

var <- "x40a_whats_the_biggest_barrier_to_you_installing_more_heat_pumps_please_select_one_option"
ids <- c(244)
replace_with <- "No barriers"

print(var)
check_variable(var, ids)
data <- recode_factor_new(var, ids, replace_with)
check_variable(var, ids)

# 54a 1

var <- "x54a_in_which_areas_could_you_improve_the_standard_of_your_heat_pump_installations"
ids <- c(451)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- replace_variable(var, ids, replace_with)
check_variable(var, ids)


# 54a 2

var <- "x54a_in_which_areas_could_you_improve_the_standard_of_your_heat_pump_installations"
ids <- c(346, 529, 589)
replace_with <- "Other - not relevant"

print(var)
check_variable(var, ids)
data <- replace_variable(var, ids, replace_with)
check_variable(var, ids)


# 54b 1

var <- "x54b_in_which_areas_could_you_improve_the_standard_of_your_heat_pump_installations"
ids <- c(689, 781, 810)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- replace_variable(var, ids, replace_with)
check_variable(var, ids)


# 54b 2

var <- "x54b_in_which_areas_could_you_improve_the_standard_of_your_heat_pump_installations"
ids <- c(830)
replace_with <- "Other - not relevant"

print(var)
check_variable(var, ids)
data <- replace_variable(var, ids, replace_with)
check_variable(var, ids)


# 56a

var <- "x56a_in_which_areas_of_your_business_do_you_use_software_apps_or_digital_tools"
ids <- c(198)
replace_with <- "Other - not relevant"

print(var)
check_variable(var, ids)
data <- replace_variable(var, ids, replace_with)
check_variable(var, ids)


# 60a

var <- "x60a_how_do_you_manage_the_design_for_the_majority_of_your_heat_pump_installations"
ids <- c(410, 451)
replace_with <- "I haven’t done any installations"

print(var)
check_variable(var, ids)
data <- recode_factor_new(var, ids, replace_with)
check_variable(var, ids)


# 70 1

var <- "x70_which_design_software_or_platform_do_you_use_select_all_that_apply"
ids <- c(763, 133, 192, 370, 529, 593, 674, 689, 796, 311, 352, 395, 589, 649)
replace_with <- "Easy MCS"

print(var)
check_variable(var, ids)
data <- replace_variable(var, ids, replace_with)
check_variable(var, ids)


# 70 2

var <- "x70_which_design_software_or_platform_do_you_use_select_all_that_apply"
ids <- c(331, 542, 616, 751, 805, 828, 300, 562, 741, 533, 309, 598)
replace_with <- "Evergreen"

print(var)
check_variable(var, ids)
data <- replace_variable(var, ids, replace_with)
check_variable(var, ids)


# 70 3

var <- "x70_which_design_software_or_platform_do_you_use_select_all_that_apply"
ids <- c(79, 621, 788, 750)
replace_with <- "H2x"

print(var)
check_variable(var, ids)
data <- replace_variable(var, ids, replace_with)
check_variable(var, ids)


# 70 4

var <- "x70_which_design_software_or_platform_do_you_use_select_all_that_apply"
ids <- c(115, 129, 144, 574, 287, 619, 821)
replace_with <- "Heatpunk"

print(var)
check_variable(var, ids)
data <- replace_variable(var, ids, replace_with)
check_variable(var, ids)


# 70 4

var <- "x70_which_design_software_or_platform_do_you_use_select_all_that_apply"
ids <- c(345, 613, 664)
replace_with <- "I don’t use design software"

print(var)
check_variable(var, ids)
data <- recode_variable(var, ids, replace_with)
check_variable(var, ids)


