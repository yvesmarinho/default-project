{% macro generate_schema_name(custom_schema_name, node) -%}
    {#-
        Custom schema naming macro.

        Default dbt behaviour:
          dev  → <user_schema>_<custom_schema>   (e.g.  john_staging)
          prod → <custom_schema>                  (e.g.  staging)

        This macro removes the user prefix in all environments,
        keeping schema names consistent across environments.

        Usage:
          In dbt_project.yml:
            models:
              my_project:
                staging:
                  +schema: staging   →  always resolves to "staging"
    -#}

    {%- set default_schema = target.schema -%}

    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}

{%- endmacro %}
