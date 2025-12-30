## Design Rationale

SAT enforces a strict internal layout because:
  
- Schemas and defaults are shared across tools
- Plugins must be discoverable in predictable locations
- Archives must never be created with incomplete metadata contracts

SAT tools are **portable**, but not **layout-agnostic** internally.

* Archives are portable.  
* The toolchain is versioned and structured.

## Future Directions

Later versions of SAT may support:
- Explicit `--sat-root` overrides
- Installed / packaged SAT runtimes
- Read-only toolchain distributions

For now, the development workflow assumes execution from a **complete SAT repository clone**.

## Summary

- SAT tools must be run from within the SAT repository
- Archives may live anywhere
- The error indicates a broken or incomplete tool layout
- This behavior is intentional and protective

When in doubt:  
**run tools from the SAT repo, point them at archives explicitly**.