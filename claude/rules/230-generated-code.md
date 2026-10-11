# Generated code and build artifacts

Do not manually edit generated files when a source, schema, template, or generator exists.

Find the source of truth.

When generated output must change:
1. change the source of truth;
2. run the generator using the repository workflow;
3. verify the generated diff.

Treat `dist/`, compiled output, generated clients, generated types, snapshots, lockfiles, and build artifacts
according to the repository's actual conventions.

Never assume a generated file is disposable or editable without checking its provenance.
