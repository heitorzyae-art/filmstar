//! The HEVC availability probe of the NVENC backend: it opens one small encoder session, once. Its own
//! test binary so that "first call" means a fresh process (driver load, Direct3D 11 device, NVENC
//! session and encoder initialisation all included).
#![cfg(target_os = "windows")]

use std::time::{Duration, Instant};

use filmstar_export::Format;
use filmstar_platform::nvenc::hevc_available;

#[test]
fn the_probe_runs_once_and_registers_the_format() {
    let t0 = Instant::now();
    let first = hevc_available();
    let cold = t0.elapsed();
    let t1 = Instant::now();
    let again = hevc_available();
    let warm = t1.elapsed();
    eprintln!("first HEVC probe in a fresh process: {cold:?} (available: {first}); the cached answer: {warm:?}");
    assert_eq!(first, again);
    assert!(warm < Duration::from_millis(50), "the answer is cached: {warm:?}");

    // `register` makes `available(Hevc)` follow the probe; registering again changes nothing
    assert!(!filmstar_export::available(Format::Hevc) || first);
    filmstar_platform::register();
    filmstar_platform::register();
    assert_eq!(filmstar_export::available(Format::Hevc), first);
    assert!(filmstar_export::available(Format::H264));
}
