from django.core.management.base import BaseCommand

from ml_engine.services import train_and_save_model


class Command(BaseCommand):
    help = (
        "Generate travel risk dataset, train the ML model, "
        "save the model artifact, calculate metrics, and "
        "register the model version."
    )

    def add_arguments(self, parser):

        parser.add_argument(
            "--model-version",
            type=str,
            default="1.0.0",
            help="Model version, for example: 1.0.0",
        )

        parser.add_argument(
            "--activate",
            action="store_true",
            help="Set this model as the active model.",
        )

    def handle(self, *args, **options):

        # IMPORTANT:
        # argparse converts --model-version to model_version
        model_version = options["model_version"]

        activate = options["activate"]

        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(
            self.style.WARNING(
                "TRAVELSHIELD V3 - ML MODEL TRAINING"
            )
        )
        self.stdout.write("=" * 60)

        self.stdout.write(
            f"Model Version: {model_version}"
        )

        self.stdout.write(
            "Starting dataset generation and model training..."
        )

        try:

            result = train_and_save_model(
                version=model_version,
                activate=activate,
            )

            self.stdout.write("")
            self.stdout.write("=" * 60)

            self.stdout.write(
                self.style.SUCCESS(
                    "MODEL TRAINING COMPLETED SUCCESSFULLY"
                )
            )

            self.stdout.write("=" * 60)

            self.stdout.write(
                f"Model Version : {result['version']}"
            )

            self.stdout.write(
                f"Dataset Rows  : {result['rows']}"
            )

            self.stdout.write(
                f"Accuracy      : {result['accuracy']}"
            )

            self.stdout.write(
                f"Precision     : {result['precision']}"
            )

            self.stdout.write(
                f"Recall        : {result['recall']}"
            )

            self.stdout.write(
                f"F1 Score      : {result['f1_score']}"
            )

            self.stdout.write("")

            self.stdout.write(
                f"Dataset Path  : {result['dataset_path']}"
            )

            self.stdout.write(
                f"Model Path    : {result['model_path']}"
            )

            self.stdout.write(
                f"Metadata Path : {result['metadata_path']}"
            )

            if activate:

                self.stdout.write("")

                self.stdout.write(
                    self.style.SUCCESS(
                        "ACTIVE MODEL: YES"
                    )
                )

        except Exception as exc:

            self.stderr.write("")

            self.stderr.write(
                self.style.ERROR(
                    "MODEL TRAINING FAILED"
                )
            )

            self.stderr.write(
                self.style.ERROR(
                    f"Error: {exc}"
                )
            )

            raise