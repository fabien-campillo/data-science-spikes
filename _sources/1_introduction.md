# Data Science & Spikes

*This Jupyter Book is designed to help you get started in data science by exploring electrophysiological data, especially spike train recordings, in a practical and accessible way.*

<br>
<br>


Even though we are mainly interested in processing electrophysiology measurements such as spikes, we will attempt an overview of neuroscience resources.

We will focus on electrophysiology data processing and distinguish between:

- M/EEG data, non-invasive/extracranial,
- and invasive data at the single neuron level or from a population of neurons, notably using MEA (Multi-Electrode Array).

*It is this second category that is of most interest to us (MathNeuro).* The first category is very well developed.
Processing extracranial electrophysiological data (EEG/MEG) is generally more complex than processing intracranial measurements (spikes, LFP, ECoG). In intracranial recordings, electrodes are close to neurons: the signal is more localized, with a better signal-to-noise ratio, which facilitates the identification of action potentials or local fields. In contrast, extracranial signals are heavily attenuated, resulting from the summation of millions of neurons and distorted by cranial tissues. They are also contaminated by numerous artifacts. Analysis therefore requires advanced processing (filtering, correction, modeling) and solving the inverse problem (retrieving brain sources from incomplete and ambiguous measurements, which is a mathematically ill-posed problem).

<br>
<br>

This Jupyter Book is part of the Data Science Bootcamp for [MathNeuro](https://team.inria.fr/mathneuro/) and is made openly accessible to the broader community.

See also the GitHub repository [https://github.com/fabien-campillo/data-science-spikes](https://github.com/fabien-campillo/data-science-spikes).


*Several parts of this book, including sections of the Markdown content and Python source code, were generated or refined with the assistance of **ChatGPT-4**, which also provided guidance on building this Jupyter Book. While this tool was helpful in drafting and organizing content, all remaining errors and final decisions are entirely my own.*


<hr style="border: 1px solid black;">

By [Fabien Campillo](https://www-sop.inria.fr/members/Fabien.Campillo/)  <br>
© Copyright 2025. This work is licensed under CC BY-NC-SA 4.0 (Creative Commons Attribution-NonCommercial-ShareAlike).