import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MedecinService } from './localisation.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-localisation-med',
  standalone: false,
  templateUrl: './localisation-med.component.html',
  styleUrls: ['./localisation-med.component.css'],
  providers: [MedecinService]
})
export class LocalisationMedComponent implements OnInit {
  adresseForm!: FormGroup;
  currentAddress = '';
  emailMedecin: string = '';

  constructor(
    private fb: FormBuilder,
    private medecinService: MedecinService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.adresseForm = this.fb.group({
      adresseActuelle: ['', Validators.required],
      nouvelleAdresse: ['', Validators.required]
    });

    this.route.queryParamMap.subscribe(params => {
      this.emailMedecin = params.get('mail') || '';

      if (this.emailMedecin) {
        // Une fois qu'on a l'email, on récupère l'adresse
        this.medecinService.getAdresseActuelle(this.emailMedecin).subscribe(adresse => {
          this.currentAddress = adresse;
          this.adresseForm.patchValue({ adresseActuelle: adresse });
        });
      } else {
        console.error('Email du médecin non trouvé dans l\'URL.');
      }
    });
  }

  valider(): void {
    const nouvelleAdresse = this.adresseForm.get('nouvelleAdresse')?.value;

    if (confirm('Vous voulez vraiment changer votre adresse ?')) {
      this.medecinService.updateAdresse(nouvelleAdresse, this.emailMedecin ).subscribe(() => {
        alert('Adresse de cabinet mise à jour avec succès.');
        
      });
    }
  }
}

