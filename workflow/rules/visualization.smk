rule grm_heatmap:
  input: grm = f"{config['build_directory']}/{{name}}/{{dims}}dims/{{distance_method}}.grm.csv",
  output: file = f"{config['results_directory']}/{{name}}/{{dims}}dims/{{distance_method}}_heatmap.png"
  script: 
    "../scripts/grm_csv_heatmap.R"


rule grm_histogram:
  input: grm = f"{config['build_directory']}/{{name}}/{{dims}}dims/{{distance_method}}.grm.csv",
  output: file = f"{config['results_directory']}/{{name}}/{{dims}}dims/{{distance_method}}_histogram.png"
  script: 
    "../scripts/grm_csv_histogram.R"


# rule grm_to_tsv:
#   input: grm = f"{config['build_directory']}/{{name}}_merged.grm",
#   output: file = f"{config['build_directory']}/{{name}}.csv"
#   script: 
#     "../scripts/grm_to_csv.R"
