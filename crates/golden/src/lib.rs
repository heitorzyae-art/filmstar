//! Golden-image tests for FilmStar's renderer (test-only crate; the library is empty).
//!
//! `tests/golden.rs` builds small procedural projects (no media files), renders one frame of each
//! through the CPU reference compositor (`filmstar-render`) and compares it with a committed PNG
//! in `goldens/` using `filmstar_testkit::golden`. The same scenes are composited on the GPU
//! (`filmstar-gpu`) when an adapter is available and compared with the CPU result.
//!
//! Regenerate references with `FILMSTAR_BLESS=1 cargo test -p filmstar-golden`.
